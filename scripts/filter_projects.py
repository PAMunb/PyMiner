import csv

# Arquivos de entrada e saída
input_file = "results.csv"
output_file = "filtered-results.csv"
csv_file_path = "../python-projects.csv"
filtered_projects = "filtered_projects.csv"

# comando abaixo gera a lista a partir do collections-failed
# tail -n +4 collections-failed.txt | awk -F"[',]" '{print $2}' | sort -u

# lista de projetos que estão presentes em projects_cloc_metrics.csv mas não em filtered_projects.csv. 
# comm -23 <(cut -d',' -f1 projects_cloc_metrics.csv | sort) <(cut -d',' -f1 filtered_projects.csv | sort)

# Lista de nomes de projetos a serem removidos
# 19 por checkout-conflicts, exceptions ou que estão fora do intervalo buscado 2012-2024
# 118 eliminados pela análise de quartis e com menos de 55 files
# totalizando 125 repositórios únicos removidos das analises.

projects_failed = (
    "barrucadu_dotfiles|4am-robotics_cob_command_tools|python-jsonschema_jsonschema|git-big-picture_git-big-picture"
)

# cob_command_tools,couchbase-python-client,open_exoplanet_catalogue,metpy,pyfreenet,goatools,ajenti,fondinfo,starcal,theharvester

projects_interval = (
    "couchbase_couchbase-python-client|openexoplanetcatalogue_open_exoplanet_catalogue|"
    "swirhen_anime-podcast|unidata_metpy|fabric|hyphanet_pyfreenet|cartridge|"
    "tanghaibao_goatools|nickjcroucher_gubbins|ajenti_ajenti|tomamic_fondinfo|"
    "starcal|4am-robotics_cob_common|laramies_theharvester|wbond_package_control_channel"
)


# Converte listas de projetos em um conjunto único
projects_set = set()
for project_list in [projects_failed, projects_interval]:
    projects_set.update(project_list.split("|"))


filtered_repos = []
with open(filtered_projects, newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        filtered_repos.append(row["project"].strip())

repositories = []
removed_repositories = []
with open(csv_file_path, newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        repository_info = {"owner": row["name"].split('/')[0], "repo": row["name"].split('/')[1]}
        file_path = f"results/{repository_info['owner']}_{repository_info['repo']}.csv"
        if repository_info['repo'] in filtered_repos:
            repositories.append(repository_info)
        else:
            removed_repositories.append(repository_info['repo'])
            
total_removed = set()
for project_list2 in [projects_set,removed_repositories]:
    total_removed.update(project_list2)            
            
print(f"Total de projetos a serem removidos: {len(total_removed)}")


wrote_lines = set()
# Filtrar linhas no arquivo de entrada
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        
        if "project,date,commit_hash,files," in line and line not in wrote_lines:
            outfile.write(line)
            wrote_lines.add(line)
            
        # Extrai o nome do projeto (assume que o nome é a primeira coluna, separada por vírgulas)
        project_name = line.split(",")[0].strip()
            
        for repo_info in repositories:
            owner = repo_info["owner"]
            repo = repo_info["repo"]            

            file_path = f"{owner}_{repo}"
            
            if (project_name == repo or project_name == file_path) and repo.strip() not in projects_set and project_name not in projects_set and repo.strip() not in removed_repositories and line not in wrote_lines:
                outfile.write(line)
                wrote_lines.add(line)
                break

print(f"Linhas filtradas foram salvas em {output_file}")