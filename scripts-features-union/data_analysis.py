import sys
import pandas as pd
from tabulate import tabulate
import seaborn as sns
import matplotlib.pyplot as plt

# Carregue os dados
df = pd.read_csv('results-without-gaps.csv')

# Lista de colunas a serem removidas
columns_to_drop = [
    'commit_hash', 'errors',
    'async_list_comprehensions_files',
    'async_set_comprehensions_files',
    'async_dict_comprehensions_files',
    'async_generator_expressions_files',
    'matrix_multiplication_files',
    'async_def_files',
    'await_expressions_files',
    'async_for_files',
    'async_with_files',
    'fstring_files',
    'except_star_files',
    'pattern_match_files',
    'pattern_as_files',
    'pattern_or_files',
    'pattern_sequence_files',
    'pattern_mapping_files',
    'pattern_class_files',
    'pattern_value_files',
    'pattern_singleton_files',
    'pattern_star_files',
    'assign_unpack_files',
    'list_unpack_files',
    'tuple_unpack_files',
    'set_unpack_files',
    'dict_unpack_files',
    'call_kwargs_unpack_files',
    'call_args_unpack_files',
    'nonlocal_files',
    'function_args_annotation_files',
    'function_return_annotation_files',
    'kw_defaults_files',
    'kw_args_files',
    'type_vars_bounds_files',
    'type_vars_constraints_files',
    'type_param_spec_files',
    'type_var_tuple_files',
    'yield_from_files',
    'assignment_expression_files',
    'suppressing_exception_context_files',
    'variable_annotation_files'
]

df = df.drop(columns=columns_to_drop)

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Dicionário de mapeamento de features
features_mapping = {
    'async_list_comprehensions': 'Asynchronous Comprehensions',
    'async_set_comprehensions': 'Asynchronous Comprehensions',
    'async_dict_comprehensions': 'Asynchronous Comprehensions',
    'async_generator_expressions': 'Asynchronous Generators',
    'matrix_multiplication': 'Matrix Multiplication',
    'async_def': 'Coroutines (async and await syntax)',
    'await_expressions': 'Coroutines (async and await syntax)',
    'async_for': 'Coroutines (async and await syntax)',
    'async_with': 'Coroutines (async and await syntax)',
    'fstring': 'Formatted String Literals (f-strings)',
    'except_star': 'Exception Groups (except *)',
    'pattern_match': 'Structural Pattern Matching',
    'pattern_as': 'Structural Pattern Matching',
    'pattern_or': 'Structural Pattern Matching',
    'pattern_sequence': 'Structural Pattern Matching',
    'pattern_mapping': 'Structural Pattern Matching',
    'pattern_class': 'Structural Pattern Matching',
    'pattern_value': 'Structural Pattern Matching',
    'pattern_singleton': 'Structural Pattern Matching',
    'pattern_star': 'Structural Pattern Matching',
    'assign_unpack': 'Extended Iterable Unpacking',
    'list_unpack': 'Additional Unpacking Generalizations',
    'tuple_unpack': 'Additional Unpacking Generalizations',
    'set_unpack': 'Additional Unpacking Generalizations',
    'dict_unpack': 'Additional Unpacking Generalizations',
    'call_kwargs_unpack': 'Additional Unpacking Generalizations',
    'call_args_unpack': 'Additional Unpacking Generalizations',
    'nonlocal': 'Nonlocal Statements',
    'function_args_annotation': 'Function Annotations',
    'function_return_annotation': 'Function Annotations',
    'kw_defaults': 'Keyword-only Arguments',
    'kw_args': 'Keyword-only Arguments',
    'type_vars_bounds': 'Type Parameter Syntax',
    'type_vars_constraints': 'Type Parameter Syntax',
    'type_param_spec': 'Type Parameter Syntax',
    'type_var_tuple': 'Type Parameter Syntax',
    'yield_from': 'Yield From Expression',
    'assignment_expression': 'Assignment Expression',
    'suppressing_exception_context': 'Suppressing Exception Context',
    'variable_annotation': 'Variable Annotation'
}


df.rename(columns=features_mapping, inplace=True)

# Visualizar as novas colunas
# print(df.columns)


last_revision_idx = df.groupby(['project'])['date'].idxmax()

df_last_revision = df.loc[last_revision_idx]

# Defina as variáveis de interesse
id_vars = ["project", "date", "statements", "files"]
value_name = "total"
var_name = "feature"

# Derreta o DataFrame para o formato apropriado
melted_df = pd.melt(df_last_revision, id_vars=id_vars, value_name=value_name, var_name=var_name)


# Mapear as features para suas categorias
# melted_df['feature'] = melted_df['feature'].map(features_mapping)

# Converta a coluna 'date' para datetime
melted_df['date'] = melted_df['date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce'))

# Converta a coluna 'value' para um tipo numérico
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

melted_df = melted_df.sort_values(by='date')


summary = melted_df.groupby('feature')['total'].agg(['median', 'mean', 'std', 'max', 'min']).reset_index()

summary['feature'] = summary['feature'].replace(features_mapping)


tablefmt = 'latex_booktabs'  # Formato LaTeX
colalign = ("l", "r", "r", "r", "r", "r")

# Agora você pode continuar com a criação da tabela LaTeX
table_summary = tabulate(summary, headers='keys', tablefmt=tablefmt, colalign=colalign)

print(table_summary)
# sys.exit()
# Filter out features with median equal to 0
nonzero_median_summary = summary[summary['median'] != 0]

# Create the boxplot
sns.boxplot(x='feature', y='total', data=melted_df[melted_df['feature'].isin(nonzero_median_summary['feature'])])
# Add labels
plt.xlabel('Features')
plt.ylabel('Total')

# Calculate median by feature for non-zero features
# medians = nonzero_median_summary.set_index('feature')['median']

# # Add median labels to the plot
# for feature, median in medians.items():
#     plt.text(x=feature, y=median, s=round(median, 2), ha='center', va='bottom')

# plt.xticks(rotation=45)

# plt.show()


pd.set_option('display.float_format', '{:.3f}'.format)
melted_df['total'] = melted_df['total'].astype(int)
total_by_feature = melted_df.groupby('feature')['total'].sum().reset_index()

# print(total_by_feature)

total_projects = df['project'].nunique()

print("Total de projetos: ",total_projects)

list_unique_projects = set()
for proj in df['project']:
    list_unique_projects.add(proj)
    
# for p in list_unique_projects:
#     print(p)

# Verificar se a feature tem pelo menos uma ocorrência
df_feature_counts = melted_df.groupby('feature')['total'].sum().reset_index()
df_filtered = df_feature_counts[df_feature_counts['total'] > 0]

# Contar a quantidade de projetos com pelo menos uma ocorrência em cada feature
df_project_counts = melted_df[melted_df['total'] > 0].groupby('feature')['project'].nunique().reset_index()
df_project_counts.columns = ['feature', 'projects_with_occurrences']

# print(df_project_counts)
summary_project_features = df_filtered.merge(df_project_counts, on='feature', how='left')

summary_project_features['percentage (%)'] = (summary_project_features['projects_with_occurrences'] / total_projects) * 100
summary_project_features = summary_project_features[['feature', 'percentage (%)']]

# print(summary_project_features)

#first adoption
id_vars = ["project", "date", "statements", "files"]
value_name = "total"
var_name = "feature"

df_first_revision = pd.melt(df, id_vars=id_vars, value_name=value_name, var_name=var_name)

# df_first_revision['feature'] = df_first_revision['feature'].map(features_mapping)

# Converta a coluna 'date' para datetime
df_first_revision['date'] = df_first_revision['date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce'))

# Converta a coluna 'value' para um tipo numérico
df_first_revision['total'] = pd.to_numeric(df_first_revision['total'], errors='coerce')

df_first_revision['year_month'] = df_first_revision['date'].dt.strftime('%Y-%m')

df_first_revision = df_first_revision.sort_values(by='year_month')

df_filtered = df_first_revision[df_first_revision['total'] > 0]

start_adoption = df_filtered.groupby('feature')['year_month'].min().reset_index()

# print(start_adoption)

total_by_feature.set_index('feature', inplace=True)
summary_project_features.set_index('feature', inplace=True)
start_adoption.set_index('feature', inplace=True)

# Mesclar os DataFrames usando a coluna "feature" como índice
merged_df = total_by_feature.merge(summary_project_features, left_index=True, right_index=True)
merged_df = merged_df.merge(start_adoption, left_index=True, right_index=True).reset_index()

# print(merged_df)

# Remover as colunas duplicadas "feature"
# merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

# Definir a coluna "feature" como índice do DataFrame resultante
merged_df.set_index('feature', inplace=True)

# print(merged_df)

# Renomear o índice para 'Feature'
merged_df.index.name = 'Feature'

# Crie uma lista com os novos nomes das colunas na ordem desejada
table_columns = ['Total of Occurrences (#)', 'Projects Adoption (%)', 'First Occurrence']



# Renomear as colunas
merged_df.columns = table_columns

# print(merged_df)

# Renomear os valores na coluna 'Feature' usando o mapeamento
# merged_df.index = merged_df.index.map(features_mapping)

merged_df = merged_df.sort_values(by='Projects Adoption (%)',ascending=False)

tablefmt = 'latex_booktabs'  # Formato LaTeX
colalign = ("right", "right", "right", "right")


# Agora você pode continuar com a criação da tabela LaTeX
table = tabulate(merged_df, headers='keys', tablefmt=tablefmt, colalign=colalign)

print(table)
