import ast
from datetime import datetime
import os
from pydriller import Repository
from git import Repo

repo_url = 'https://github.com/conda/conda.git'
path = 'dataset/'

repo_name = Repository(repo_url)._get_repo_name_from_url(repo_url)

clone_path = path+repo_name

repo_commits = []
for commit in Repository(repo_url, since=datetime(2024, 1, 1)).traverse_commits():
    repo_commits.append(commit.hash)
    # print(f'Commit {commit.hash}, {commit.author_date}')
    # print(f'Autor: {commit.author.name}')
    # print(f'Data: {commit.author_date}')
    # print(f'Mensagem: {commit.msg}')
    # print('--------------------------')
print("Total de commits: ",len(repo_commits))

if not os.path.exists(clone_path):
    Repo.clone_from(repo_url, clone_path)

repo = Repo(clone_path)

repo_files = []

for commit in repo_commits:
    repo.git.checkout(commit)
    print(f'Commit: {commit}')
    repo_files = [os.path.relpath(os.path.join(dirpath,file), start=clone_path) 
                 for dirpath, dirnames, files in os.walk(clone_path) 
                 for file in files if file.endswith('.py')]
    if(len(repo_files) > 0):
        print("Total de arquivos:", len(repo_files))
        # print(f'Arquivos no commit {commit}:')
        # for file in repo_files:
        #     print(f'- {file}')
        # break
    
repo_path = repo.working_tree_dir

def find_and_print_match_nodes(node):
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.While):
            print(f'Encontrado node While: {ast.dump(sub_node, annotate_fields=True, indent=4)}')    
    
for file in repo_files:
    # print(f'Arquivo: {file}')
    file_path = os.path.join(repo_path, file)
    try:
        # Abrindo e lendo o conteúdo do arquivo
        with open(file_path, 'r') as f:
            file_content = f.read()

        # Parseando o código para obter a árvore AST
        parsed_code = ast.parse(file_content)
        ast_tree = ast.dump(parsed_code, annotate_fields=True, indent=4)
        
        # Encontrar e imprimir nós Match
        find_and_print_match_nodes(parsed_code)
    
    except Exception as e:
        # Em caso de exceção, imprime o nome do arquivo e o conteúdo do arquivo
        # print(f'Erro ao processar o arquivo: {file}')
        # print(f'Conteúdo do arquivo:\n{file_content}')
        print(f'Erro: {e}')
        # print('--------------------------')
