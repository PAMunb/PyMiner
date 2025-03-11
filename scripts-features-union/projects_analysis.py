import pandas as pd
from tabulate import tabulate

# Carregue os dados
df = pd.read_csv('projects_cloc_metrics.csv')

# Remova as colunas 'comments' e 'blank_lines'
df = df.drop(columns=['comments', 'blank_lines'])

id_vars = ["code_lines"]
value_name = "total"
var_name = "project"

# Derreta o DataFrame para o formato apropriado
melted_df = pd.melt(df, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Converter a coluna 'total' para valores numéricos, tratando valores não numéricos como NaN
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

# Remover linhas com valores ausentes (NaN)
melted_df = melted_df.dropna(subset=['total'])

# Calcule as estatísticas resumidas
summary = melted_df.groupby('project')['total'].agg(['median', 'mean', 'std', 'max', 'min']).reset_index()

# Especifique o formato da tabela LaTeX
tablefmt = 'latex_booktabs'  # Formato LaTeX
colalign = ("l", "r", "r", "r", "r", "r")

# Crie a tabela LaTeX
table_summary = tabulate(summary, headers='keys', tablefmt=tablefmt, colalign=colalign)

# Imprima a tabela LaTeX
print(table_summary)


id_vars = ["files"]
value_name = "total"
var_name = "project"

# Derreta o DataFrame para o formato apropriado
melted_df = pd.melt(df, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Converter a coluna 'total' para valores numéricos, tratando valores não numéricos como NaN
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

# Remover linhas com valores ausentes (NaN)
melted_df = melted_df.dropna(subset=['total'])

# Defina uma função de formatação personalizada para exibir números inteiros sem notação científica
def format_int(x):
    return f'{x:.0f}'

# Defina a opção de formatação de ponto flutuante para usar a função de formatação personalizada
pd.set_option('display.float_format', format_int)

# Calcule as estatísticas resumidas
summary = melted_df.groupby('project')['total'].agg(['median', 'mean', 'std', 'max', 'min']).reset_index()

# Especifique o formato da tabela LaTeX
tablefmt = 'latex_booktabs'  # Formato LaTeX
colalign = ("l", "r", "r", "r", "r", "r")

# Crie a tabela LaTeX
table_summary = tabulate(summary, headers='keys', tablefmt=tablefmt, colalign=colalign)

# Imprima a tabela LaTeX
print(table_summary)

pd.reset_option('display.float_format')
