import sys
import pandas as pd
import os
import csv

def verificar_anos_em_csv(diretorio):
    # Lista para armazenar os nomes dos projetos que não atendem aos critérios
    projetos_nao_adequados = []

    # Função auxiliar para verificar se uma string é uma data válida
    def eh_data_valida(data_string):
        try:
            pd.to_datetime(data_string, format='%Y-%m-%d', errors='raise')
            return True
        except ValueError:
            return False

    # Função para ler CSV e filtrar linhas malformadas
    def ler_csv_filtrado(caminho, num_colunas):
        linhas_validas = []
        with open(caminho, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            cabecalho = next(csvreader)
            # print(len(cabecalho))

            for linha in csvreader:
                # print(len(linha))
                if linha and linha[-1] == '':
                    linha.pop()
                if len(linha) == num_colunas:
                    linhas_validas.append(linha)
        df = pd.DataFrame(linhas_validas, columns=cabecalho)
        return df

    # Percorrer todos os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            # Construir o caminho completo do arquivo
            caminho_arquivo = os.path.join(diretorio, arquivo)

            # Definir o número de colunas esperadas
            num_colunas = 96

            # Ler o arquivo CSV filtrando linhas malformadas
            try:
                df = ler_csv_filtrado(caminho_arquivo, num_colunas)
            except Exception as e:
                print(f"Erro ao processar o arquivo {caminho_arquivo}: {e}")
                continue

            # Verificar se o arquivo possui linhas suficientes
            if len(df) > 1:
                # print(df)
                # sys.exit()
                # Verificar a data da primeira linha após o cabeçalho
                data_primeira_linha = df.iloc[0]['date']
                if eh_data_valida(data_primeira_linha):
                    ano_primeira_linha = pd.to_datetime(data_primeira_linha, format='%Y-%m-%d').year
                else:
                    ano_primeira_linha = None

                # Verificar a data da última linha do arquivo
                data_ultima_linha = df.iloc[-1]['date']
                if eh_data_valida(data_ultima_linha):
                    ano_ultima_linha = pd.to_datetime(data_ultima_linha, format='%Y-%m-%d').year
                else:
                    ano_ultima_linha = None
                # Verificar os anos das datas
                print(f"Ano da primeira linha: {ano_primeira_linha}, ano da última linha: {ano_ultima_linha}")
                if ano_primeira_linha != 2012 or ano_ultima_linha != 2024:
                    # Adicionar o nome do projeto à lista se os critérios não forem atendidos
                    projetos_nao_adequados.append(df.iloc[0]['project'])

    # Imprimir os nomes dos projetos que não atendem aos critérios
    if projetos_nao_adequados:
        print("Projetos que não atendem aos critérios:")
        for projeto in projetos_nao_adequados:
            print(projeto)
    else:
        print("Todos os projetos atendem aos critérios.")

# Definir o diretório onde os arquivos CSV estão localizados
diretorio_csv = '../results/'

# Chamar a função para verificar os arquivos CSV no diretório
verificar_anos_em_csv(diretorio_csv)
