# Script Python para contar linhas por projeto

filename = 'collections-failed.txt'  # substitua pelo nome do seu arquivo

project_counts = {}

with open(filename, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Começa a leitura a partir da quarta linha (índice 3)
for line in lines[3:]:
    line = line.strip()
    if line.startswith('['):
        # Avalia a string para uma lista python
        line_data = eval(line)
        project_name = line_data[0]
        # Incrementa o contador do projeto
        project_counts[project_name] = project_counts.get(project_name, 0) + 1

# Ordena o resultado em ordem decrescente de quantidade de linhas
sorted_projects = sorted(project_counts.items(), key=lambda x: x[1], reverse=True)

# Imprime o resultado final
for project, count in sorted_projects:
    print(f"Projeto: {project}, Quantidade de linhas: {count}")
