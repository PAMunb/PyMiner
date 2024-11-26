#!/bin/bash

# Diretório onde os repositórios devem estar clonados
REPOS_DIR="../dataset/"

# Arquivo CSV que contém os nomes dos repositórios
CSV_FILE="../python-projects.csv"

# Função para verificar se um repositório foi clonado
check_repo_cloned() {
  repo_name=$1
  repo_dir="$REPOS_DIR/$repo_name"

  if [ -d "$repo_dir" ]; then
    # echo "Clonado: $repo_name"
    continue
  else
    echo "Não clonado: $repo_name"
  fi
}

# Ler o arquivo CSV e verificar cada repositório
tail -n +2 "$CSV_FILE" | while IFS=, read -r id name isFork commits branches defaultBranch releases contributors license watchers stargazers forks size createdAt pushedAt updatedAt homepage mainLanguage totalIssues openIssues totalPullRequests openPullRequests blankLines codeLines commentLines metrics lastCommit lastCommitSHA hasWiki isArchived languages labels topics; do
  # Remover aspas duplas do nome do repositório e capturar a parte após a barra
  repo_name=$(echo "$name" | tr -d '"' | awk -F/ '{print $2}')
  
  # Chamar a função para verificar se o repositório foi clonado
  check_repo_cloned "$repo_name"
done
