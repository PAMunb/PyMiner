import os
import csv
import subprocess
import json

def obter_estatisticas_projeto(diretorio_projeto):
    # Execute o comando cloc para obter as estatísticas do projeto
    resultado_cloc = subprocess.run(['cloc', '--include-lang=Python', '--json', diretorio_projeto], capture_output=True, text=True)
    
    # Verifique se o comando cloc foi executado com sucesso
    if resultado_cloc.returncode != 0:
        print(f"Erro ao executar cloc no projeto {diretorio_projeto}: {resultado_cloc.stderr}")
        return {}
    
    # Analise o JSON de saída do cloc para obter as estatísticas desejadas
    json_cloc = resultado_cloc.stdout
    if not json_cloc.strip():
        print(f"Nenhum resultado JSON do cloc para o projeto {diretorio_projeto}")
        return {}

    estatisticas = {}
    try:
        estatisticas = obter_estatisticas_do_json(json_cloc)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON do cloc para o projeto {diretorio_projeto}: {e}")
        print(f"Saída do cloc: {json_cloc}")
    
    return estatisticas

def obter_estatisticas_do_json(json_cloc):
    # Analise o JSON do cloc e obtenha as estatísticas desejadas
    estatisticas = {}
    dados_cloc = json.loads(json_cloc)
    
    if 'SUM' in dados_cloc:
        sum_data = dados_cloc['SUM']
        estatisticas['files'] = sum_data.get('nFiles', 0)
        estatisticas['blank_lines'] = sum_data.get('blank', 0)
        estatisticas['comments'] = sum_data.get('comment', 0)
        estatisticas['code_lines'] = sum_data.get('code', 0)
    
    return estatisticas

def gerar_csv(lista_projetos, arquivo_csv):
    # Escreva as estatísticas em um arquivo CSV
    with open(arquivo_csv, 'w', newline='') as csvfile:
        campos = ['project', 'files', 'blank_lines', 'comments', 'code_lines']
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        
        # Escreva o cabeçalho
        writer.writeheader()
        
        # Escreva as estatísticas para cada projeto
        for projeto in lista_projetos:
            print("Analisando projeto:", projeto)
            estatisticas = obter_estatisticas_projeto(projeto)
            estatisticas['project'] = os.path.basename(projeto)
            writer.writerow(estatisticas)

# Diretório contendo várias pastas de projetos do GitHub
diretorio_base = r'../dataset'

# Lista de projetos (subdiretórios)
projetos = [os.path.join(diretorio_base, projeto) for projeto in os.listdir(diretorio_base) if os.path.isdir(os.path.join(diretorio_base, projeto))]

# Arquivo CSV de saída
arquivo_csv_saida = r'projects_cloc_metrics.csv'

# Gere o CSV com as estatísticas para cada projeto
gerar_csv(projetos, arquivo_csv_saida)
