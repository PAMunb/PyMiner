#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import sys
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import re
from datetime import datetime

import ast
import io
import tokenize
import pandas as pd

# =========================================================
#exemplo para verificar paramentros execute - python3 report.py -h

#exemplo para executar
"""python report.py   
--results-csv results.csv  
--results results   
--dataset dataset   
--repos-csv manifest.csv  
--out out   
--csv-glob "*_matches.csv"   
--since 2020-06-01  
--structural-pickaxe  
"""
# =========================================================

# =========================================================
# util git / fs
# =========================================================

def run(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def is_git_repo(path: Path) -> bool:
    p = run(["git", "rev-parse", "--is-inside-work-tree"], cwd=path)
    return p.returncode == 0 and p.stdout.strip() == "true"

def git_clone_or_update(dst: Path, url: str, fresh: bool = False) -> bool:
    if fresh and dst.exists():
        try:
            shutil.rmtree(dst)
        except Exception:
            return False
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        p = run(["git", "clone", "--no-checkout", url, str(dst)])
        if p.returncode != 0:
            return False
    p = run(["git", "fetch", "--all", "--tags", "--prune"], cwd=dst)
    return p.returncode == 0

def git_blame_line(repo: Path, commit: str, file: str, lineno: int) -> Optional[str]:
    p = run(["git", "blame", "-l", "-s", "-L", f"{lineno},{lineno}", commit, "--", file], cwd=repo)
    if p.returncode != 0:
        return None
    line = (p.stdout or "").strip().splitlines()
    if not line:
        return None
    first = line[0].split()[0]
    if re.fullmatch(r"[0-9a-fA-F]{7,40}", first):
        return first
    return None

def git_show_file(repo: Path, commit: str, file: str) -> Optional[str]:
    p = run(["git", "show", f"{commit}:{file}"], cwd=repo)
    return p.stdout if p.returncode == 0 else None

def git_commit_date(repo: Path, commit: str) -> Optional[str]:
    p = run(["git", "show", "-s", "--format=%cI", commit], cwd=repo)
    return p.stdout.strip() if p.returncode == 0 else None

def git_log_search_match(repo: Path, file: str, since_iso: Optional[str], structural: bool = True) -> List[str]:
    """
    Retorna SHAs (newest..oldest) de commits que tocam linhas com `match` no arquivo.
    structural=True usa -G '^[[:space:]]*match[[:space:]].*:' (foca no statement).
    """
    if structural:
        pattern = r'^[[:space:]]*match[[:space:]].*:'
        args = ["git", "log", "--format=%H", "-G", pattern]
    else:
        args = ["git", "log", "--format=%H", "-S", "match"]
    if since_iso:
        args.extend([f"--since={since_iso}"])
    args.extend(["--", file])
    p = run(args, cwd=repo)
    if p.returncode != 0:
        return []
    return [line.strip() for line in p.stdout.splitlines() if line.strip()]

def git_file_history(repo: Path, file: str) -> List[str]:
    p = run(["git", "log", "--follow", "--format=%H", "--", file], cwd=repo)
    if p.returncode != 0:
        return []
    return [line.strip() for line in p.stdout.splitlines() if line.strip()]

def first_match_lineno_in_blob(text: str) -> int:
    for i, line in enumerate(text.splitlines(), start=1):
        if re.search(r"(?i)\bmatch\b", line):
            return i
    return -1

# =========================================================
# diff parsing e heurísticas de rejuvenescimento
# =========================================================

HUNK_RE = re.compile(r"@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? \+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@")

@dataclass
class DiffLine:
    tag: str       # ' ', '+', '-'
    text: str
    old_no: Optional[int]
    new_no: Optional[int]

@dataclass
class Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: List[DiffLine]

def parse_unified_diff_for_file(repo: Path, commit: str, file: str) -> List[Hunk]:
    """
    Parseia `git show <commit> -- <file>` em hunks com numeração de linhas antiga/novas.
    """
    p = run(["git", "show", commit, "--", file], cwd=repo)
    if p.returncode != 0:
        return []
    hunks: List[Hunk] = []
    old_no = new_no = None
    cur: Optional[Hunk] = None
    for raw in p.stdout.splitlines():
        m = HUNK_RE.match(raw.strip())
        if m:
            # inicia nova hunk
            old_start = int(m.group("old_start"))
            old_count = int(m.group("old_count") or 1)
            new_start = int(m.group("new_start"))
            new_count = int(m.group("new_count") or 1)
            cur = Hunk(old_start, old_count, new_start, new_count, [])
            hunks.append(cur)
            old_no = old_start
            new_no = new_start
            continue
        if cur is None:
            continue
        if not raw:
            # linha vazia de diff (trata como contexto)
            cur.lines.append(DiffLine(' ', "", old_no, new_no))
            if old_no is not None: old_no += 1
            if new_no is not None: new_no += 1
            continue
        tag = raw[0]
        text = raw[1:] if len(raw) > 1 else ""
        if tag == ' ':
            cur.lines.append(DiffLine(' ', text, old_no, new_no))
            if old_no is not None: old_no += 1
            if new_no is not None: new_no += 1
        elif tag == '-':
            cur.lines.append(DiffLine('-', text, old_no, None))
            if old_no is not None: old_no += 1
        elif tag == '+':
            cur.lines.append(DiffLine('+', text, None, new_no))
            if new_no is not None: new_no += 1
        else:
            # outras linhas (--- +++ index ...) ignorar dentro da hunk
            pass
    return hunks

def added_match_lines(hunk: Hunk) -> List[DiffLine]:
    # linha de código 'match' statement: começa com match e termina com ':'
    out = []
    for dl in hunk.lines:
        if dl.tag == '+' and re.search(r'^\s*match\b.*:\s*$', dl.text):
            out.append(dl)
    return out

def added_case_count(hunk: Hunk) -> int:
    return sum(1 for dl in hunk.lines if dl.tag == '+' and re.search(r'^\s*case\b', dl.text))

def removed_if_lines(hunk: Hunk) -> List[DiffLine]:
    return [dl for dl in hunk.lines if dl.tag == '-' and re.search(r'^\s*(if|elif|else)\b', dl.text)]

MATCH_SUBJECT_RE = re.compile(r'^\s*match\s+(?P<expr>[^:]+):\s*$')

def extract_match_subject(text_line: str) -> str:
    m = MATCH_SUBJECT_RE.search(text_line)
    return m.group('expr').strip() if m else ""

def hunk_text_before_after(hunk: Hunk) -> Tuple[str, str]:
    before = "\n".join(("-" + dl.text) for dl in hunk.lines if dl.tag == '-')
    after  = "\n".join(("+" + dl.text) for dl in hunk.lines if dl.tag == '+')
    return before, after

def detect_direct_rejuvenations(repo: Path, commit: str, file: str) -> List[dict]:
    res = []
    for idx, h in enumerate(parse_unified_diff_for_file(repo, commit, file)):
        added = added_match_lines(h)
        removed = removed_if_lines(h)
        if added and removed:
            subj = extract_match_subject(added[0].text)
            before, after = hunk_text_before_after(h)
            rec = {
                "method": "direct",
                "commit_insert": commit,
                "window_commit": commit,
                "hunk_index": idx,
                "subject_expr": subj,
                "removed_if_count": len(removed),
                "added_case_count": added_case_count(h),
                "before_lineno_min": min([dl.old_no or 0 for dl in removed]) if removed else "",
                "after_lineno_min": min([dl.new_no or 0 for dl in added]) if added else "",
                "code_before": before,
                "code_after": after,
            }
            res.append(rec)
    return res

def detect_window_rejuvenations(
    repo: Path,
    file: str,
    commit_insert: str,
    subject_expr: str,
    history_commits: List[str],
    window_prev: int,
    window_next: int
) -> List[dict]:
    """
    Procura remoções de if/elif/else em commits próximos ao de inserção.
    Faz *matching* textual simples pelo subject_expr.
    """
    if not history_commits:
        return []
    try:
        i = history_commits.index(commit_insert)
    except ValueError:
        # se não achar, considerar toda a lista
        i = 0
    # janela: commits mais antigos (i+1, i+2, ...) e mais novos (..., i-1)
    candidates: List[Tuple[str, str]] = []  # (commit, direction)
    # antes (mais antigos): i+1 .. i+window_prev
    for c in history_commits[i+1:i+1+window_prev]:
        candidates.append((c, "before"))
    # depois (mais novos): i-1 .. i-window_next
    for c in history_commits[max(0, i-window_next):i][::-1]:
        candidates.append((c, "after"))

    out = []
    for c, direction in candidates:
        for idx, h in enumerate(parse_unified_diff_for_file(repo, c, file)):
            rem = removed_if_lines(h)
            if not rem:
                continue
            # Se tiver subject_expr, exigir que ele apareça em alguma linha removida
            if subject_expr and not any(subject_expr in (dl.text or "") for dl in rem):
                continue
            before, _after_dummy = hunk_text_before_after(h)
            rec = {
                "method": "window",
                "commit_insert": commit_insert,
                "window_commit": c,
                "hunk_index": idx,
                "subject_expr": subject_expr,
                "removed_if_count": len(rem),
                "added_case_count": "",  # não olhamos cases aqui (são do commit de inserção)
                "before_lineno_min": min([dl.old_no or 0 for dl in rem]) if rem else "",
                "after_lineno_min": "",
                "code_before": before,
                "code_after": "",  # será preenchido pelo commit de inserção (abaixo)
                "direction": direction,
            }
            out.append(rec)
    return out

# =========================================================
# análise de comentários/docstrings
# =========================================================

def _docstring_and_string_spans(py_source: str) -> Tuple[Dict[int, List[Tuple[int, int]]], Dict[int, List[Tuple[int, int]]]]:
    doc_start_lines: set = set()
    try:
        t = ast.parse(py_source)
        if t.body and isinstance(t.body[0], ast.Expr) and isinstance(getattr(t.body[0], 'value', None), ast.Constant) and isinstance(t.body[0].value.value, str):
            ln = getattr(t.body[0], 'lineno', 0) or 0
            if ln:
                doc_start_lines.add(ln)
        class V(ast.NodeVisitor):
            def _maybe_doc(self, node):
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], 'value', None), ast.Constant) and isinstance(node.body[0].value.value, str):
                    ln = getattr(node.body[0], 'lineno', 0) or 0
                    if ln:
                        doc_start_lines.add(ln)
            def visit_FunctionDef(self, node): self._maybe_doc(node); self.generic_visit(node)
            def visit_AsyncFunctionDef(self, node): self._maybe_doc(node); self.generic_visit(node)
            def visit_ClassDef(self, node): self._maybe_doc(node); self.generic_visit(node)
        V().visit(t)
    except SyntaxError:
        pass

    doc_spans: Dict[int, List[Tuple[int, int]]] = {}
    str_spans: Dict[int, List[Tuple[int, int]]] = {}

    def add_span(d: Dict[int, List[Tuple[int, int]]], line: int, s: int, e: int):
        d.setdefault(line, []).append((s, e))

    try:
        for tok in tokenize.generate_tokens(io.StringIO(py_source).readline):
            if tok.type != tokenize.STRING:
                continue
            sline, scol = tok.start
            eline, ecol = tok.end
            is_doc = (sline in doc_start_lines)
            target = doc_spans if is_doc else str_spans
            if sline == eline:
                add_span(target, sline, scol, ecol)
            else:
                add_span(target, sline, scol, 10**9)
                for ln in range(sline + 1, eline):
                    add_span(target, ln, 0, 10**9)
                add_span(target, eline, 0, ecol)
    except tokenize.TokenError:
        pass

    return doc_spans, str_spans

def _classify_match_lines(py_source: str) -> List[Tuple[int, str]]:
    """
    Classifica cada linha que contém a palavra 'match' em:
    {'docstring','string_literal','comment','code'}.
    """
    doc_spans, str_spans = _docstring_and_string_spans(py_source)

    comment_cols: Dict[int, List[Tuple[int, int]]] = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(py_source).readline):
            if tok.type == tokenize.COMMENT:
                sline, scol = tok.start
                eline, ecol = tok.end
                comment_cols.setdefault(sline, []).append((scol, ecol))
    except tokenize.TokenError:
        pass

    out: List[Tuple[int, str]] = []
    for i, line in enumerate(py_source.splitlines(), start=1):
        m = re.search(r"(?i)\bmatch\b", line)
        if not m:
            continue
        ms = m.start()
        # docstring?
        for s, e in doc_spans.get(i, []):
            if s <= ms < e:
                out.append((i, 'docstring'))
                break
        else:
            # string literal?
            for s, e in str_spans.get(i, []):
                if s <= ms < e:
                    out.append((i, 'string_literal'))
                    break
            else:
                # comentário?
                for s, e in comment_cols.get(i, []):
                    if s <= ms < e:
                        out.append((i, 'comment'))
                        break
                else:
                    out.append((i, 'code'))
    return out

# =========================================================
# carga e normalização dos *_matches.csv / results.csv
# =========================================================

def load_projects_with_match(results_csv: Path) -> List[str]:
    df = pd.read_csv(results_csv)
    pm_col = None
    for c in df.columns:
        if c.lower().strip() == "pattern_match":
            pm_col = c
            break
    if pm_col is None:
        raise RuntimeError("results.csv precisa da coluna 'pattern_match'.")
    proj_col = None
    for c in df.columns:
        if c.lower().strip() in {"project", "projeto", "repo", "repository", "name"}:
            proj_col = c
            break
    if proj_col is None:
        raise RuntimeError("results.csv precisa ter coluna de projeto (ex.: 'project').")
    projs = (
        df.loc[df[pm_col] > 0, proj_col]
        .dropna()
        .astype(str)
        .map(lambda s: s.strip())
        .unique()
        .tolist()
    )
    return projs

def find_match_csvs(results_dir: Path, allowed_projects: Iterable[str], glob_pattern: str = "*_matches.csv") -> List[Path]:
    allowed_set = {p.lower() for p in allowed_projects}
    paths = sorted(results_dir.rglob(glob_pattern))
    out: List[Path] = []
    for p in paths:
        name_l = p.name.lower()
        parent_l = p.parent.name.lower()
        chosen = False
        for proj in allowed_set:
            if proj and (proj in name_l or proj in parent_l):
                out.append(p)
                chosen = True
                break
        if not chosen and not allowed_set:
            out.append(p)
    return out

def read_rows_from_match_csv(path: Path, project_hint: Optional[str] = None) -> pd.DataFrame:
    tried: List[Tuple[str, str]] = [(",", "utf-8"), (";", "utf-8"), (",", "latin-1"), (";", "latin-1")]
    last_err = None
    df = None
    for sep, enc in tried:
        try:
            df = pd.read_csv(path, sep=sep, encoding=enc)
            break
        except Exception as e:
            last_err = e
    if df is None:
        raise RuntimeError(f"Falha lendo {path}: {last_err}")

    cols_map = {c.lower().strip(): c for c in df.columns}
    def get_col(key: str, aliases: List[str]) -> Optional[str]:
        for k in [key] + aliases:
            if k in cols_map:
                return cols_map[k]
        return None

    c_commit = get_col("commit", ["sha", "revision"]) or "commit"
    c_file = get_col("file", ["filepath", "path", "filename"]) or "file"
    c_line = get_col("lineno", ["line", "line_no", "line_number"]) or "lineno"
    c_proj = get_col("project", ["projeto", "repo", "repository"]) or None

    out = pd.DataFrame()
    out["commit"] = df[c_commit] if c_commit in df.columns else None
    out["file"] = df[c_file] if c_file in df.columns else None
    if c_line in df.columns:
        out["lineno"] = pd.to_numeric(df[c_line], errors="coerce").fillna(-1).astype(int)
    else:
        out["lineno"] = -1

    if c_proj and c_proj in df.columns:
        out["project"] = df[c_proj].astype(str)
    else:
        proj = project_hint or path.parent.name
        out["project"] = proj

    out["source_csv"] = str(path)
    return out.dropna(subset=["commit", "file"]).reset_index(drop=True)

# =========================================================
# mapeamentos de repositórios e since
# =========================================================

def parse_repo_overrides(items: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for it in items:
        if not it:
            continue
        if "=" in it:
            k, v = it.split("=", 1)
        elif ":" in it:
            k, v = it.split(":", 1)
        else:
            print(f"[AVISO] --repo malformado: '{it}' (use project=url)")
            continue
        out[k.strip()] = v.strip()
    return out

@dataclass
class RepoSpec:
    project: str
    url: str

def load_repos_map(repos_csv: Optional[Path]) -> Dict[str, str]:
    if repos_csv is None:
        return {}
    df = pd.read_csv(repos_csv)
    cols_map = {c.lower().strip(): c for c in df.columns}
    c_proj = cols_map.get("project") or cols_map.get("projeto") or cols_map.get("repo") or cols_map.get("name")
    c_url = cols_map.get("repo_url") or cols_map.get("url")
    if not c_proj or not c_url:
        raise RuntimeError("repos.csv deve conter colunas: project, repo_url")
    mapping = {str(p).strip(): str(u).strip() for p, u in zip(df[c_proj], df[c_url]) if pd.notna(p) and pd.notna(u)}
    return mapping

def load_since_map(since_csv: Optional[Path], default_since: str) -> Dict[str, str]:
    m: Dict[str, str] = {}
    if since_csv and since_csv.exists():
        df = pd.read_csv(since_csv)
        cols_map = {c.lower().strip(): c for c in df.columns}
        c_proj = cols_map.get("project") or cols_map.get("projeto") or cols_map.get("repo") or cols_map.get("name")
        c_since = cols_map.get("since") or cols_map.get("date")
        if c_proj and c_since:
            for p, s in zip(df[c_proj], df[c_since]):
                if pd.notna(p) and pd.notna(s):
                    m[str(p).strip()] = str(s).strip()
    m.setdefault("*", default_since)
    return m

def decide_since_for_project(project: str, since_map: Dict[str, str]) -> str:
    return since_map.get(project, since_map.get("*", "2020-06-01"))

# =========================================================
# main
# =========================================================

def main():
    ap = argparse.ArgumentParser(description="Consolida commits de matches, timeline, comentados e rejuvenescimentos (direct/window)")
    ap.add_argument("--results-csv", type=Path, default=None, help="CSV com projects e pattern_match (obrigatório exceto no modo --test-*)")
    ap.add_argument("--results", type=Path, default=None, help="Pasta com *_matches.csv (obrigatório exceto no modo --test-*)")
    ap.add_argument("--dataset", type=Path, required=True, help="Pasta onde os repositórios serão clonados/atualizados")
    ap.add_argument("--repos-csv", type=Path, default=None, help="CSV com mapping: project,repo_url (opcional)")
    ap.add_argument("--repo", action="append", default=[], help="Mapeamento pontual project=url (pode repetir)")
    ap.add_argument("--skip-clone", action="store_true", help="Não clonar/atualizar; usar repositórios já existentes em dataset/")
    ap.add_argument("--out", type=Path, default=Path("out"), help="Pasta de saída (CSV)" )
    ap.add_argument("--csv-glob", type=str, default="*_matches.csv", help="Glob para localizar CSVs de matches")
    ap.add_argument("--since", type=str, default="2020-06-01", help="Data ISO-8601 global (início da busca de inserções)")
    ap.add_argument("--since-csv", type=Path, default=None, help="CSV opcional com colunas project,since (sobrepõe --since por projeto)")
    ap.add_argument("--fresh-clone", action="store_true", help="Reclonar repositórios do zero")
    ap.add_argument("--structural-pickaxe", action="store_true", help="Usa -G '^[[:space:]]*match[[:space:]].*:' em vez de -S match para achar commits")
    ap.add_argument("--all-insertions", action="store_true", help="Capturar TODAS as inserções de match por arquivo (não só a primeira)")
    ap.add_argument("--window-prev", type=int, default=5, help="Commits para trás na janela de rejuvenescimento (indireto)")
    ap.add_argument("--window-next", type=int, default=3, help="Commits para frente na janela de rejuvenescimento (indireto)")
    # modo teste
    ap.add_argument("--test-project", type=str, default=None)
    ap.add_argument("--test-file", type=str, default=None)
    ap.add_argument("--test-commit", type=str, default=None)
    ap.add_argument("--test-dump", action="store_true")
    args = ap.parse_args()

    ensure_dir(args.out)
    ensure_dir(args.dataset)

    # ------------- MODO TESTE -------------
    if args.test_project and args.test_file and args.test_commit:
        repos_map = load_repos_map(args.repos_csv)
        repos_map.update(parse_repo_overrides(args.repo))
        proj = args.test_project
        repo_dir = args.dataset / proj
        if not (repo_dir.exists() and is_git_repo(repo_dir)) and not args.skip_clone:
            url = repos_map.get(proj) or repos_map.get(proj.lower()) or repos_map.get(proj.upper())
            if not url:
                print(f"[ERRO] Repo '{proj}' não encontrado e sem URL.")
                sys.exit(5)
            if not git_clone_or_update(repo_dir, url, fresh=args.fresh_clone):
                print(f"[ERRO] Falha ao clonar {proj}")
                sys.exit(6)

        blob = git_show_file(repo_dir, args.test_commit, args.test_file)
        if not blob:
            print(f"[ERRO] Não consegui abrir {args.test_file} no commit {args.test_commit}.")
            sys.exit(7)
        cls = _classify_match_lines(blob)
        hits = [(ln, cat) for (ln, cat) in cls if cat in {"docstring", "comment"}]
        lines = blob.splitlines()
        out_rows = []
        for ln, cat in hits:
            start = max(0, ln-3); end = min(len(lines), ln+7)
            snippet = "\n".join(lines[start:end])
            out_rows.append({
                "project": proj, "file": args.test_file, "commit": args.test_commit,
                "lineno": ln, "categoria": cat, "code_snippet": snippet,
            })
        out_test = args.out / "teste_projetos_comentados.csv"
        pd.DataFrame(out_rows, columns=["project","file","commit","lineno","categoria","code_snippet"]).to_csv(out_test, index=False)
        print(f"[TESTE] Linhas com 'match' em comentário/docstring no commit {args.test_commit}: {len(out_rows)}")
        print(f"[TESTE] Resultado salvo em {out_test}")
        return

    # ------------- ENTRADAS OBRIGATÓRIAS -------------
    if not (args.results_csv and args.results):
        print("ERRO: --results-csv e --results são obrigatórios fora do modo --test-*")
        sys.exit(2)

    # 1) Filtra projetos
    projects = load_projects_with_match(args.results_csv)
    print(f" - Projetos filtrados (pattern_match>0): {len(projects)}")
    projects_l = [p.lower() for p in projects]

    # 2) Encontra *_matches.csv
    match_csvs = find_match_csvs(args.results, projects, args.csv_glob)
    if not match_csvs:
        print("ERRO: Nenhum *_matches.csv encontrado para os projetos filtrados.")
        sys.exit(2)
    print(f"CSVs de match detectados: {len(match_csvs)}")

    # 3) Lê linhas
    dfs: List[pd.DataFrame] = []
    for p in match_csvs:
        proj_hint = None
        name_l = p.name.lower(); parent_l = p.parent.name.lower()
        for proj in projects_l:
            if proj in name_l or proj in parent_l:
                proj_hint = proj; break
        dfp = read_rows_from_match_csv(p, project_hint=proj_hint)
        dfp["project_norm"] = dfp["project"].astype(str).str.lower().str.strip()
        dfp = dfp[dfp["project_norm"].isin(projects_l)]
        if not dfp.empty:
            dfs.append(dfp.drop(columns=["project_norm"]))
    if not dfs:
        print("ERRO: Não há linhas nos *_matches.csv para os projetos filtrados.")
        sys.exit(3)

    all_rows = pd.concat(dfs, ignore_index=True)
    all_rows["commit"] = all_rows["commit"].astype(str)
    all_rows["file"] = all_rows["file"].astype(str)
    all_rows["project"] = all_rows["project"].astype(str)

    # 4) Clona/atualiza repositórios
    repos_map = load_repos_map(args.repos_csv)
    repos_map.update(parse_repo_overrides(args.repo))

    cloned_ok = present_ok = skipped = 0
    cloned_list: List[str] = []; present_list: List[str] = []; skipped_list: List[str] = []

    for proj in sorted(set(all_rows["project"])):
        repo_dir = args.dataset / proj
        url = repos_map.get(proj) or repos_map.get(proj.lower()) or repos_map.get(proj.upper())
        if args.skip_clone:
            if repo_dir.exists() and is_git_repo(repo_dir):
                present_ok += 1; present_list.append(proj)
            else:
                print(f"[AVISO] Repo ausente para '{proj}' e --skip-clone ativo; pulando.")
                skipped += 1; skipped_list.append(proj)
        else:
            if url:
                if git_clone_or_update(repo_dir, url, fresh=args.fresh_clone):
                    cloned_ok += 1; cloned_list.append(proj); print(f"[CLONE] {proj} -> OK")
                else:
                    print(f"[ERRO] Falha ao clonar/atualizar {proj} ({url})"); skipped += 1; skipped_list.append(proj)
            else:
                if repo_dir.exists() and is_git_repo(repo_dir):
                    present_ok += 1; present_list.append(proj)
                else:
                    print(f"[AVISO] Sem URL para '{proj}' e repo não existe; pulando.")
                    skipped += 1; skipped_list.append(proj)

    print(f"Repositórios: clonados/atualizados={cloned_ok}, já_presentes={present_ok}, pulados={skipped}")
    if cloned_list:  print(" - Clonados/atualizados:", ", ".join(sorted(cloned_list)))
    if present_list: print(" - Já presentes:", ", ".join(sorted(present_list)))
    if skipped_list: print(" - Pulados:", ", ".join(sorted(skipped_list)))

    # 5) Datas
    dates: List[str] = []
    for _, row in all_rows.iterrows():
        repo_dir = args.dataset / row["project"]
        d = git_commit_date(repo_dir, row["commit"]) if repo_dir.exists() and is_git_repo(repo_dir) else None
        dates.append(d or "")
    all_rows["commit_date"] = dates

    # 6) Timeline
    def parse_iso(s: str) -> datetime:
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return datetime.min
    all_rows["_dt"] = [parse_iso(s) for s in all_rows["commit_date"]]
    timeline = all_rows.sort_values(["project", "file", "_dt"]).drop(columns=["_dt"])
    out_timeline = args.out / "commits_timeline.csv"
    timeline.to_csv(out_timeline, index=False)
    print(f"OK: timeline salvo em {out_timeline}")

    # 6.1) Resumo projetos
    proj_summary = (
        timeline.groupby("project").agg(
            files=("file", "nunique"),
            commits=("commit", "nunique"),
            first_date=("commit_date", lambda x: min([d for d in x if isinstance(d, str) and d], default="")),
            last_date=("commit_date", lambda x: max([d for d in x if isinstance(d, str) and d], default="")),
        ).reset_index()
    )
    out_proj = args.out / "projetos_consolidados.csv"
    proj_summary.to_csv(out_proj, index=False)
    projetos_consolidados = sorted(proj_summary["project"].astype(str).tolist())
    print(f"OK: projetos consolidados salvos em {out_proj}")
    print("Projetos consolidados:", ", ".join(projetos_consolidados) if projetos_consolidados else "(nenhum)")

    # 7) Inserções de match por arquivo (primeira ou todas)
    since_map = load_since_map(args.since_csv, args.since)
    insercoes_records: List[Dict[str, str]] = []

    for (proj, file), grp in timeline.groupby(["project", "file"], sort=False):
        repo_dir = args.dataset / proj
        if not (repo_dir.exists() and is_git_repo(repo_dir)):
            continue
        since_iso = decide_since_for_project(proj, since_map)
        commits_touching = git_log_search_match(repo_dir, file, since_iso, structural=args.structural_pickaxe)
        if not commits_touching:
            head_commit = grp.iloc[-1]["commit"]
            blob = git_show_file(repo_dir, head_commit, file)
            if blob and re.search(r"^\s*match\b.*:\s*$", blob, flags=re.M):
                ln = first_match_lineno_in_blob(blob)
                insercoes_records.append({
                    "project": proj, "file": file,
                    "commit_insert": head_commit,
                    "commit_date": git_commit_date(repo_dir, head_commit) or "",
                    "lineno_guess": str(ln),
                    "code_snippet": "\n".join(blob.splitlines()[max(0, ln-3):ln+7]) if ln>0 else "",
                })
            continue

        # oldest..newest
        
        chain = list(reversed(commits_touching))
        if not args.all_insertions:
            chain = chain[:1]  # só a primeira inserção após --since

        for c in chain:
            blob = git_show_file(repo_dir, c, file) or ""
            ln = first_match_lineno_in_blob(blob) if blob else -1
            snippet = "\n".join(blob.splitlines()[max(0, ln-3):ln+7]) if ln > 0 else ""
            insercoes_records.append({
                "project": proj, "file": file,
                "commit_insert": c,
                "commit_date": git_commit_date(repo_dir, c) or "",
                "lineno_guess": str(ln),
                "code_snippet": snippet,
            })

    insercoes_df = pd.DataFrame(insercoes_records, columns=[
        "project", "file", "commit_insert", "commit_date", "lineno_guess", "code_snippet"
    ])
    out_inserts = args.out / "insercoes_match_unicas.csv"
    insercoes_df.to_csv(out_inserts, index=False)
    print(f"OK: inserções salvas em {out_inserts}")

    # 8) Projetos comentados (comentário/docstring/string_literal)
    comentados_records: List[Dict[str, str]] = []
    files_df = (
        all_rows.sort_values(["project", "file"])
        .dropna(subset=["file", "commit"])
        .groupby(["project", "file"], as_index=False).first()
    )
    seen_file: set = set()
    for _, row in files_df.iterrows():
        proj = str(row["project"]); file = str(row["file"])
        if (proj, file) in seen_file:
            continue
        seen_file.add((proj, file))
        repo_dir = args.dataset / proj
        if not (repo_dir.exists() and is_git_repo(repo_dir)):
            continue
        commit = str(row["commit"]) or ""
        if not commit:
            continue
        blob = git_show_file(repo_dir, commit, file) or ""
        if not blob:
            continue
        classified = _classify_match_lines(blob)
        noncode = [(ln, cat) for (ln, cat) in classified if cat in {"docstring", "comment", "string_literal"}]
        if not noncode:
            continue
        # escolhe a primeira por prioridade (comment > docstring > string_literal)
        pri = {"comment": 0, "docstring": 1, "string_literal": 2}
        noncode.sort(key=lambda t: (pri.get(t[1], 9), t[0]))
        ln, categoria = noncode[0]
        blame_sha = git_blame_line(repo_dir, commit, file, ln) or ""
        lines = blob.splitlines()
        start = max(0, ln-3); end = min(len(lines), ln+7)
        snippet = "\n".join(lines[start:end])
        comentados_records.append({
            "project": proj, "file": file, "commit": commit,
            "commit_date": git_commit_date(repo_dir, commit) or "",
            "lineno": ln, "categoria": categoria,
            "code_snippet": snippet, "line_text": lines[ln-1] if 1<=ln<=len(lines) else "",
            "added_here": (blame_sha.lower()==commit.lower()),
            "blame_commit": blame_sha,
        })

    comentados_df = pd.DataFrame(comentados_records, columns=[
        "project","file","commit","commit_date","lineno","categoria","code_snippet","line_text","added_here","blame_commit"
    ])
    out_coment = args.out / "projetos_comentados.csv"
    comentados_df.to_csv(out_coment, index=False)
    print(f"OK: projetos comentados salvos em {out_coment} (total arquivos considerados: {len(files_df)}; registros: {len(comentados_df)})")

    # 9) Rejuvenescimentos (direct/window)
    rejuvenesc_records: List[Dict[str, str]] = []
    for _, row in insercoes_df.iterrows():
        proj = str(row["project"]); file = str(row["file"]); cinsert = str(row["commit_insert"])
        repo_dir = args.dataset / proj
        if not (repo_dir.exists() and is_git_repo(repo_dir)):
            continue

        # DIRECT
        direct = detect_direct_rejuvenations(repo_dir, cinsert, file)
        # extrair subject e after do commit de inserção (pra enriquecer "window")
        subj = ""
        after_for_window = ""
        after_cases = 0
        if direct:
            # usa o primeiro como referência
            subj = direct[0].get("subject_expr","") or ""
            # (já vamos salvar cada hunk abaixo)
        else:
            # pegar after_for_window a partir de uma hunk com match (mesmo que não tenha if removido)
            for h in parse_unified_diff_for_file(repo_dir, cinsert, file):
                adds = added_match_lines(h)
                if adds:
                    subj = extract_match_subject(adds[0].text)
                    _b, _a = hunk_text_before_after(h)
                    after_for_window = _a
                    after_cases = added_case_count(h)
                    break

        for d in direct:
            rejuvenesc_records.append({
                "project": proj, "file": file,
                "method": d["method"],
                "commit_insert": cinsert,
                "commit_insert_date": git_commit_date(repo_dir, cinsert) or "",
                "window_commit": d["window_commit"],
                "window_commit_date": git_commit_date(repo_dir, d["window_commit"]) or "",
                "hunk_index": d["hunk_index"],
                "subject_expr": d["subject_expr"],
                "removed_if_count": d["removed_if_count"],
                "added_case_count": d["added_case_count"],
                "before_lineno_min": d["before_lineno_min"],
                "after_lineno_min": d["after_lineno_min"],
                "code_before": d["code_before"],
                "code_after": d["code_after"],
            })

        # WINDOW (só se não houve direct)
        if not direct:
            history = git_file_history(repo_dir, file)
            window_hits = detect_window_rejuvenations(
                repo=repo_dir, file=file, commit_insert=cinsert,
                subject_expr=subj, history_commits=history,
                window_prev=args.window_prev, window_next=args.window_next
            )
            for w in window_hits:
                rejuvenesc_records.append({
                    "project": proj, "file": file,
                    "method": w["method"],
                    "commit_insert": cinsert,
                    "commit_insert_date": git_commit_date(repo_dir, cinsert) or "",
                    "window_commit": w["window_commit"],
                    "window_commit_date": git_commit_date(repo_dir, w["window_commit"]) or "",
                    "hunk_index": w["hunk_index"],
                    "subject_expr": w["subject_expr"],
                    "removed_if_count": w["removed_if_count"],
                    "added_case_count": after_cases,
                    "before_lineno_min": w["before_lineno_min"],
                    "after_lineno_min": "",
                    "code_before": w["code_before"],
                    "code_after": after_for_window,
                })

    rejuvenesc_df = pd.DataFrame(rejuvenesc_records, columns=[
        "project","file","method","commit_insert","commit_insert_date",
        "window_commit","window_commit_date","hunk_index","subject_expr",
        "removed_if_count","added_case_count","before_lineno_min","after_lineno_min",
        "code_before","code_after"
    ])
    out_rejuv = args.out / "rejuvenescimentos.csv"
    rejuvenesc_df.to_csv(out_rejuv, index=False)
    print(f"OK: rejuvenescimentos salvos em {out_rejuv} (total registros: {len(rejuvenesc_df)})")

    # 10) Log textual
    out_log = args.out / "log_consolidacao.txt"
    with out_log.open("w", encoding="utf-8") as fh:
        fh.write("# Log da consolidação de matches\n")
        fh.write(f"Projetos filtrados (pattern_match>0): {len(projects)}\n")
        fh.write("Projetos filtrados: " + ", ".join(sorted(projects)) + "\n")
        fh.write(f"CSVs de match considerados: {len(match_csvs)}\n")
        for pth in match_csvs[:50]:
            fh.write(f" - {pth}\n")
        if len(match_csvs) > 50:
            fh.write(f" ... (+{len(match_csvs)-50} mais)\n")
        fh.write(f"Projetos consolidados: {len(projetos_consolidados)}\n")
        fh.write("Projetos consolidados: " + ", ".join(projetos_consolidados) + "\n")
        fh.write(f"Repositórios clonados/atualizados ({len(cloned_list)}): " + ", ".join(sorted(cloned_list)) + "\n")
        fh.write(f"Repositórios já presentes ({len(present_list)}): " + ", ".join(sorted(present_list)) + "\n")
        fh.write(f"Repositórios pulados ({len(skipped_list)}): " + ", ".join(sorted(skipped_list)) + "\n")
        fh.write("Saídas geradas:\n")
        fh.write(f" - {out_timeline}\n - {out_proj}\n - {out_inserts}\n - {out_coment}\n - {out_rejuv}\n")
    print(f"OK: log salvo em {out_log}")

    # 11) Resumo
    print("Resumo:")
    print(f" - Projetos filtrados (pattern_match>0): {len(projects)}")
    print(f" - CSVs de match considerados: {len(match_csvs)}")
    print(f" - Linhas consolidadas: {len(all_rows)}")
    print(f" - Repositórios clonados/atualizados: {cloned_ok}")
    print(f" - Repositórios já presentes: {present_ok}")
    print(f" - Repositórios pulados: {skipped}")
    print(f" - Arquivos com inserção detectada: {len(insercoes_df)}")
    print(f" - Rejuvenescimentos (direct/window): {len(rejuvenesc_df)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)
