#!/bin/bash

# Arquivo de entrada
input_file="results.csv"
# Arquivo de saída
output_file="filtered-results.csv"

# comando abaixo gera a lista a partir do collections-failed
# tail -n +4 collections-failed.txt | awk -F"[',]" '{print $2}' | sort -u

# Lista de nomes de projetos a serem removidos
# 9 por checkout-conflicts and exceptions
projects="4am-robotics_cob_common|barrucadu_dotfiles|hyphanet_pyfreenet|nickjcroucher_gubbins|openexoplanetcatalogue_open_exoplanet_catalogue|python-jsonschema_jsonschema|swirhen_anime-podcast|tomamic_fondinfo|wbond_package_control_channel"

# Filtra as linhas que não correspondem ao padrão
grep -Ev "^($projects)," "$input_file" > "$output_file"

echo "Linhas filtradas foram salvas em $output_file"