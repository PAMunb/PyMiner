#!/bin/bash

# Caminho do diretório que será limpo
DIR="dataset"

# Verifica se o diretório existe
if [ -d "$DIR" ]; then
  echo "Limpando o diretório $DIR, mantendo apenas .gitignore e .gitkeep..."

  # Remove todos os arquivos, exceto .gitignore e .gitkeep
  find "$DIR" -type f ! -name '.gitignore' ! -name '.gitkeep' -exec rm -f {} +

  # Remove todos os subdiretórios dentro de dataset/
  find "$DIR" -mindepth 1 -type d -exec rm -rf {} +

  echo "Limpeza concluída."
else
  echo "O diretório $DIR não existe."
fi

# find results/ -type f -name "*.csv" -exec rm {} \;
