#!/bin/bash

# Arquivo de entrada
input_file="results.csv"
# Arquivo de saída
output_file="filtered-results.csv"

# Lista de nomes de projetos a serem removidos
# 36 por checkout-conflicts and exceptions
projects="4am-robotics_cob_common|openexoplanetcatalogue_open_exoplanet_catalogue|barrucadu_dotfiles|swirhen_anime-podcast|zomojo_compiletools|linuxmint_mintupdate|opencadc_vostools|phpbb_documentation|ytdl-org_youtube-dl|ipa320_cob_robots|hivesolutions_colony|mozilla_mozregression|reactionmechanismgenerator_rmg-database|mavlink_mavlink|neurodebian_neurodebian|datadog_dd-agent|hyphanet_pyfreenet|mozilla-releng_balrog|reviewboard_rbtools|walterdejong_synctool|wbond_package_control_channel|nickjcroucher_gubbins|proycon_folia|spaam_svtplay-dl|clusterlabs_pcs|reactionmechanismgenerator_rmg-py|ipa320_cob_simulation|wbond_package_control|coderholic_pyradio|fls-bioinformatics-core_genomics|openmc-dev_openmc|nicolargo_glances|nixos_nixops|tomamic_fondinfo|andreafrancia_trash-cli|git-big-picture_git-big-picture"

# Filtra as linhas que não correspondem ao padrão
grep -Ev "^($projects)," "$input_file" > "$output_file"

echo "Linhas filtradas foram salvas em $output_file"