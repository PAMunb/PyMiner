import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ruptures as rpt


# -----------------------------
# 1) Leitura e preparação (mais simples)
# -----------------------------
df = pd.read_csv("results-without-gaps.csv")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"]).copy()
df["year_month"] = df["date"].dt.to_period("M").astype(str)

# Mapeia colunas *_files -> nome da feature
features_mapping = {
    "async_list_comprehensions_files": "Asynchronous Comprehensions",
    "async_set_comprehensions_files": "Asynchronous Comprehensions",
    "async_dict_comprehensions_files": "Asynchronous Comprehensions",
    "async_generator_expressions_files": "Asynchronous Generators",
    "matrix_multiplication_files": "Matrix Multiplication",
    "async_def_files": "Coroutines (async and await syntax)",
    "await_expressions_files": "Coroutines (async and await syntax)",
    "async_for_files": "Coroutines (async and await syntax)",
    "async_with_files": "Coroutines (async and await syntax)",
    "fstring_files": "Formatted String Literals (f-strings)",
    "pattern_match_files": "Structural Pattern Matching",
    "pattern_as_files": "Structural Pattern Matching",
    "pattern_or_files": "Structural Pattern Matching",
    "pattern_sequence_files": "Structural Pattern Matching",
    "pattern_mapping_files": "Structural Pattern Matching",
    "pattern_class_files": "Structural Pattern Matching",
    "pattern_value_files": "Structural Pattern Matching",
    "pattern_singleton_files": "Structural Pattern Matching",
    "pattern_star_files": "Structural Pattern Matching",
    "assign_unpack_files": "Extended Iterable Unpacking",
    "list_unpack_files": "Additional Unpacking Generalizations",
    "tuple_unpack_files": "Additional Unpacking Generalizations",
    "set_unpack_files": "Additional Unpacking Generalizations",
    "dict_unpack_files": "Additional Unpacking Generalizations",
    "call_kwargs_unpack_files": "Additional Unpacking Generalizations",
    "call_args_unpack_files": "Additional Unpacking Generalizations",
    "nonlocal_files": "Nonlocal Statements",
    "function_args_annotation_files": "Function Annotations",
    "function_return_annotation_files": "Function Annotations",
    "kw_defaults_files": "Keyword-only Arguments",
    "kw_args_files": "Keyword-only Arguments",
    "type_vars_bounds_files": "Type Parameter Syntax",
    "type_vars_constraints_files": "Type Parameter Syntax",
    "type_param_spec_files": "Type Parameter Syntax",
    "type_var_tuple_files": "Type Parameter Syntax",
    "yield_from_files": "Yield From Expression",
    "assignment_expression_files": "Assignment Expression",
    "suppressing_exception_context_files": "Suppressing Exception Context",
    "variable_annotation_files": "Variable Annotation",
    "except_star_files": "Except (*)",
    "exception_group_files": "ExceptionGroup",
}

# Mantém só o essencial + as colunas relevantes
keep_cols = ["project", "date", "year_month"]
keep_cols += [c for c in features_mapping.keys() if c in df.columns]
df = df[keep_cols].copy()

# Renomeia para nomes agregados (algumas features se somam depois)
df = df.rename(columns=features_mapping)

features = sorted(set(features_mapping.values()))

# Pega a última revisão de cada projeto no mês (evita duplicar mês por projeto)
last_revision_idx = (
    df.groupby(["project", "year_month"])["date"]
      .idxmax()
      .to_numpy()
)
df = df.loc[last_revision_idx].copy()

# Long format
melted = df.melt(
    id_vars=["project", "date", "year_month"],
    var_name="feature",
    value_name="total"
)
melted["total"] = pd.to_numeric(melted["total"], errors="coerce").fillna(0.0)
melted["date"] = pd.to_datetime(melted["year_month"], format="%Y-%m", errors="coerce")
melted = melted.dropna(subset=["date"]).copy()


# -----------------------------
# 2) Série mensal contínua
# -----------------------------
def monthly_series_for_feature(df_long: pd.DataFrame, feature: str) -> pd.DataFrame:
    s = (
        df_long[df_long["feature"] == feature]
        .groupby("date", as_index=False)["total"]
        .sum()
        .sort_values("date")
        .reset_index(drop=True)
    )
    if s.empty:
        return s
    full_idx = pd.date_range(s["date"].min(), s["date"].max(), freq="MS")
    s = s.set_index("date").reindex(full_idx, fill_value=0.0).rename_axis("date").reset_index()
    s["year_month"] = s["date"].dt.to_period("M").astype(str)
    return s


# -----------------------------
# 3) Detector simples e robusto (ruptures + seleção por "adoção generalizada")
# -----------------------------
def mad(x: np.ndarray) -> float:
    """Median Absolute Deviation (robusto)."""
    m = np.median(x)
    return float(np.median(np.abs(x - m)))

def detect_onset_simple(y_raw: np.ndarray) -> dict | None:
    """
    Retorna o melhor onset (índice na série mensal) ou None.
    Metodologia:
      - log1p em contagens (reduz heterocedasticidade)
      - PELT (l2) com penalty determinístico
      - escolhe o breakpoint que maximiza o ganho robusto (mediana pós - mediana pré),
        normalizado por MAD, com persistência via janelas simétricas.
    Sem parâmetros "ajustáveis" pelo usuário: min_size/horizon/pen são derivados de n.
    """
    n = len(y_raw)
    if n < 36:  # série muito curta: evitar falsas conclusões
        return None

    y = np.log1p(y_raw.astype(float))

    # Janelas derivadas do tamanho da série (determinístico, simples e estável)
    # - min_size: evita segmentos curtos
    # - horizon: janela de avaliação pré/pós para "adoção generalizada"
    min_size = max(12, n // 20)     # ~5% da série, mínimo 12 meses
    horizon  = max(12, n // 10)     # ~10% da série, mínimo 12 meses

    # Penalty determinístico (escala + log(n)).
    # Intuição: cresce com variância e com complexidade da série.
    v = float(np.var(y)) + 1e-12
    pen = 3.0 * np.log(n) * v

    algo = rpt.Pelt(model="l2", min_size=min_size, jump=1).fit(y)
    bkps = algo.predict(pen=pen)

    # candidatos = breakpoints internos (exclui o n final)
    candidates = [b for b in bkps if 0 < b < n]

    if not candidates:
        return None

    # pontuação robusta: efeito normalizado por MAD na escala log
    # e exigindo janelas completas pré e pós (persistência)
    scale = 1.4826 * mad(y)
    scale = max(scale, 1e-3)

    best = None  # (score, b, pre_med_raw, post_med_raw)
    for b in candidates:
        pre_start = b - horizon
        post_end = b + horizon
        if pre_start < 0 or post_end > n:
            continue

        pre_med = float(np.median(y[pre_start:b]))
        post_med = float(np.median(y[b:post_end]))

        # deve haver ganho sustentado
        if post_med <= pre_med:
            continue

        score = (post_med - pre_med) / scale

        # também computa na escala bruta só para log/debug/relatório
        pre_med_raw = float(np.median(y_raw[pre_start:b]))
        post_med_raw = float(np.median(y_raw[b:post_end]))

        if best is None or score > best[0]:
            best = (score, b, pre_med_raw, post_med_raw)

    if best is None:
        return None

    score, b, pre_med_raw, post_med_raw = best
    return {
        "trend_start_idx": int(b),
        "pen": float(pen),
        "min_size": int(min_size),
        "horizon": int(horizon),
        "score": float(score),
        "pre_median": float(pre_med_raw),
        "post_median": float(post_med_raw),
        "bkps": bkps,
    }


# -----------------------------
# 4) Execução + gráficos + tabela LaTeX
# -----------------------------
outdir = "graphs_onset_simple"
os.makedirs(outdir, exist_ok=True)

trend_points = []

for feature in features:
    series = monthly_series_for_feature(melted, feature)
    if series.empty:
        continue

    y_raw = series["total"].to_numpy(dtype=float)
    result = detect_onset_simple(y_raw)

    fig = plt.figure(figsize=(12, 7))
    ax = plt.gca()
    ax.plot(series["date"], series["total"], linewidth=2, label="Monthly total")

    ax.set_title(f"{feature} — Onset of generalized adoption (ruptures + median)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total occurrences (#)")

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xticks(rotation=45)

    if result is not None:
        idx = result["trend_start_idx"]
        onset_date = series.loc[idx, "date"]
        onset_ym = series.loc[idx, "year_month"]
        onset_value = float(series.loc[idx, "total"])

        ax.axvline(onset_date, linestyle="--", linewidth=2, label=f"Onset ({onset_ym})")
        ax.scatter([onset_date], [onset_value], s=60, zorder=3)

        ax.annotate(
            f"{onset_ym}\nscore={result['score']:.2f}\nH={result['horizon']}",
            xy=(onset_date, onset_value),
            xytext=(10, 10),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->"),
            fontsize=10
        )

        trend_points.append({
            "feature": feature,
            "year_month": onset_ym,
            "value": onset_value,
            "score": float(result["score"]),
            "pre_median": float(result["pre_median"]),
            "post_median": float(result["post_median"]),
            "horizon": int(result["horizon"]),
        })

    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"trend_{feature}.pdf"))
    plt.close(fig)

# Tabela LaTeX
if trend_points:
    trend_df = pd.DataFrame(trend_points).sort_values(by="year_month")

    latex = "\\begin{table}[htb]\n\\centering\n"
    latex += "\\caption{Onset of generalized adoption per feature (ruptures + median in pre/post windows).}\n"
    latex += "\\label{tab:trend_onsets_simple}\n"
    latex += "\\begin{tabular}{lccccc}\n\\toprule\n"
    latex += "Feature & Onset (Year--Month) & Total & Score & PreMed & PostMed \\\\\n\\midrule\n"

    for _, r in trend_df.iterrows():
        latex += (
            f"{r['feature']} & {r['year_month']} & {r['value']:.0f} & "
            f"{r['score']:.2f} & {r['pre_median']:.1f} & {r['post_median']:.1f} \\\\\n"
        )

    latex += "\\bottomrule\n\\end{tabular}\n\\end{table}\n"

    with open("trend_onsets_table_simple.tex", "w", encoding="utf-8") as f:
        f.write(latex)

    print("✅ Concluído. PDFs em:", outdir)
    print("✅ Tabela LaTeX salva em: trend_onsets_table_simple.tex")
else:
    print("⚠️ Nenhum onset detectado com a regra de adoção generalizada.")