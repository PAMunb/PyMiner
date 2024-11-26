import pandas as pd
import csv

data = pd.read_csv('projects_cloc_metrics.csv', encoding='latin-1')

data_sorted = data.sort_values(by='files', ascending=False)

print(data_sorted.head())

Q1 = data_sorted['files'].quantile(0.75)
Q2 = data_sorted['files'].quantile(0.5)
Q3 = data_sorted['files'].quantile(0.25) 

print("Q1:", Q1)
print("Q2:", Q2)
print("Q3:", Q3)

limite_inferior = Q3

# print("Limite Inferior:", limite_inferior)

data_filtrada = data_sorted[data_sorted['files'] >= limite_inferior]

# print(len(data_filtrada))

data_filtrada.to_csv('filtered_projects.csv', index=False, encoding='latin-1')

# Função para extrair o nome do repositório a partir do campo "name"
def extract_repo_name(name):
    return name.split('/')[1].strip()

# Caminho dos arquivos CSV
step2_csv_path = '../python-projects.csv'
filtered_projects_csv_path = 'filtered_projects.csv'

# Lista para armazenar os projetos filtrados
filtered_projects = []

# Ler o arquivo CSV de projetos filtrados
with open(filtered_projects_csv_path, newline='', encoding='latin-1') as filtered_file:
    filtered_reader = csv.DictReader(filtered_file)
    for row in filtered_reader:
        project_name = row['project'].strip()
        filtered_projects.append(project_name)

# Criar um novo arquivo CSV para os repositórios JavaScript
python_repositories_path = 'python-repositories.csv'

# Escrever o cabeçalho no arquivo CSV
with open(python_repositories_path, mode='w', newline='') as python_file:
    fieldnames = ["id", "name", "isFork", "commits", "branches", "defaultBranch", "releases", "contributors", "license",
                  "watchers", "stargazers", "forks", "size", "createdAt", "pushedAt", "updatedAt", "homepage",
                  "mainLanguage", "totalIssues", "openIssues", "totalPullRequests", "openPullRequests", "blankLines",
                  "codeLines", "commentLines", "metrics", "lastCommit", "lastCommitSHA", "hasWiki", "isArchived",
                  "isDisabled","isLocked","languages", "labels", "topics"]
    writer = csv.DictWriter(python_file, fieldnames=fieldnames)
    writer.writeheader()

    # Ler o arquivo CSV original e escrever apenas as linhas correspondentes aos projetos filtrados
    with open(step2_csv_path, newline='', encoding='latin-1') as step2_file:
        step2_reader = csv.DictReader(step2_file)
        for row in step2_reader:
            repo_name = extract_repo_name(row['name'])
            if repo_name in filtered_projects:
                writer.writerow(row)

print(f'O arquivo {python_repositories_path} foi gerado com sucesso.')