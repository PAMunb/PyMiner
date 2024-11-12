import logging
from feature_counter import FeatureCounter
from type_hint_visitor import TypeHintVisitor
import csv
import os
import sys

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    
    # Verifica se o caminho do arquivo CSV foi fornecido como argumento de linha de comando
    if len(sys.argv) < 2:
        logger.error("Por favor, forneça o caminho para o arquivo CSV como argumento de linha de comando.")
        sys.exit(1)
    
    # Caminho para o arquivo CSV
    csv_file_path = sys.argv[1]
    
    # Lista de repositórios para processar
    repositories = []

    # Lê os dados do arquivo CSV e adiciona os repositórios à lista
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            repository_info = {"owner": row["name"].split('/')[0], "repo": row["name"].split('/')[1]}
            repositories.append(repository_info)

    # Processa cada repositório
    for repo_info in repositories:
        owner = repo_info["owner"]
        repo = repo_info["repo"]
        repo_url = f"https://github.com/{owner}/{repo}.git"
        feature_counter = FeatureCounter(repo_url, [TypeHintVisitor])
        feature_counter.process()
        feature_counter.export_to_csv(f"results/{owner}_{repo}.csv")