import pandas as pd

# caminhos de entrada/saída (ajuste se quiser)
projects_csv = "python-projects.csv"
results_csv  = "scripts-features-union/filtered-results.csv"
output_csv   = "python-projects-filtered.csv"

# lê os CSVs
projects = pd.read_csv(projects_csv, dtype=str)
results  = pd.read_csv(results_csv, dtype=str)

# converte "owner_repo" -> "owner/repo"
def to_owner_repo(x: str) -> str:
    x = str(x or "").strip()
    return x.split("_", 1)[0] + "/" + x.split("_", 1)[1] if "_" in x else x

targets = (
    results["project"]
    .map(to_owner_repo)
    .str.lower().str.strip()
    .dropna()
    .unique()
)

# filtra por interseção
out = projects[
    projects["name"].str.lower().str.strip().isin(set(targets))
].copy()

# salva resultado
out.to_csv(output_csv, index=False)
print(f"Linhas escritas: {len(out)} -> {output_csv}")
