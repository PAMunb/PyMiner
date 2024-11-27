import csv

# Arquivos de entrada e saída
input_file = "dataset_projects.csv"
filtered_projects = "filtered_projects.csv"
csv_file_path = "../python-projects.csv"
        
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

        
dataset_repos = set()        
with open(input_file, newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        with open(csv_file_path, newline='') as csvfile2:
            csv_reader2 = csv.DictReader(csvfile2)
            for row2 in csv_reader2:
                repository_info = {"owner": row2["name"].split('/')[0], "repo": row2["name"].split('/')[1]}
                file_path = f"{repository_info['owner']}_{repository_info['repo']}"
                if row["project"].strip() == file_path:
                    dataset_repos.add(repository_info['repo'].strip())
                elif repository_info['repo'].strip() == row["project"].strip():
                    dataset_repos.add(repository_info['repo'].strip())
                    
                    
print(len(dataset_repos))                    

for index,rep in enumerate(dataset_repos):
    print(f"repositorio {index}: {rep}")                    
                    
output_file = set()
for repo in dataset_repos:
    if repo not in filtered_repos:
        output_file.add(repo)
            
for proj in output_file:
    print(proj)