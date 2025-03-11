import sys
import pandas as pd
from tabulate import tabulate
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Carregue os dados
df = pd.read_csv('results-without-gaps.csv')

# Filtrar as colunas de interesse
features_columns = [
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
    'type_alias_files',
    'yield_from_files',
    'assignment_expression_files',
    'suppressing_exception_context_files'
]

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

last_revision_idx = df.groupby(['project'])['date'].idxmax()

df_last_revision = df.loc[last_revision_idx]

# print(df)
# sys.exit()

# Calcular a porcentagem de arquivos com ocorrências para cada revisão
for feature in features_columns:
    df_last_revision[feature + '_percentage'] = (df_last_revision[feature] / df['files']) * 100
    

# Defina as variáveis de interesse
id_vars = ["project", "date", "commit_hash", "statements", "files"]
value_name = "total"
var_name = "feature"

df_summary = df_last_revision.drop(columns=[
        'async_list_comprehensions',
    'async_set_comprehensions',
    'async_dict_comprehensions',
    'async_generator_expressions',
    'matrix_multiplication',
    'async_def',
    'await_expressions',
    'async_for',
    'async_with',
    'fstring',
    'except_star',
    'pattern_match',
    'pattern_as',
    'pattern_or',
    'pattern_sequence',
    'pattern_mapping',
    'pattern_class',
    'pattern_value',
    'pattern_singleton',
    'pattern_star',
    'assign_unpack',
    'list_unpack',
    'tuple_unpack',
    'set_unpack',
    'dict_unpack',
    'call_kwargs_unpack',
    'call_args_unpack',
    'nonlocal',
    'function_args_annotation',
    'function_return_annotation',
    'kw_defaults',
    'kw_args',
    'type_vars_bounds',
    'type_vars_constraints',
    'type_param_spec',
    'type_var_tuple',
    'type_alias',
    'yield_from',
    'assignment_expression',
    'suppressing_exception_context',
    'type_alias'
])

df_summary = df_summary.drop(columns=[
    'errors',
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
    'type_alias_files',
    'yield_from_files',
    'assignment_expression_files',
    'suppressing_exception_context_files', 'type_alias_files_percentage'])

# print(df_summary.columns)

# Dicionário de mapeamento de features
features_mapping = {
    'async_list_comprehensions_files_percentage': 'Asynchronous Comprehensions',
    'async_set_comprehensions_files_percentage': 'Asynchronous Comprehensions',
    'async_dict_comprehensions_files_percentage': 'Asynchronous Comprehensions',
    'async_generator_expressions_files_percentage': 'Asynchronous Generators',
    'matrix_multiplication_files_percentage': 'Matrix Multiplication',
    'async_def_files_percentage': 'Coroutines (async and await syntax)',
    'await_expressions_files_percentage': 'Coroutines (async and await syntax)',
    'async_for_files_percentage': 'Coroutines (async and await syntax)',
    'async_with_files_percentage': 'Coroutines (async and await syntax)',
    'fstring_files_percentage': 'Formatted String Literals (f-strings)',
    'except_star_files_percentage': 'Exception Groups (except *)',
    'pattern_match_files_percentage': 'Structural Pattern Matching',
    'pattern_as_files_percentage': 'Structural Pattern Matching',
    'pattern_or_files_percentage': 'Structural Pattern Matching',
    'pattern_sequence_files_percentage': 'Structural Pattern Matching',
    'pattern_mapping_files_percentage': 'Structural Pattern Matching',
    'pattern_class_files_percentage': 'Structural Pattern Matching',
    'pattern_value_files_percentage': 'Structural Pattern Matching',
    'pattern_singleton_files_percentage': 'Structural Pattern Matching',
    'pattern_star_files_percentage': 'Structural Pattern Matching',
    'assign_unpack_files_percentage': 'Extended Iterable Unpacking',
    'list_unpack_files_percentage': 'Additional Unpacking Generalizations',
    'tuple_unpack_files_percentage': 'Additional Unpacking Generalizations',
    'set_unpack_files_percentage': 'Additional Unpacking Generalizations',
    'dict_unpack_files_percentage': 'Additional Unpacking Generalizations',
    'call_kwargs_unpack_files_percentage': 'Additional Unpacking Generalizations',
    'call_args_unpack_files_percentage': 'Additional Unpacking Generalizations',
    'nonlocal_files_percentage': 'Nonlocal Statements',
    'function_args_annotation_files_percentage': 'Function Annotations',
    'function_return_annotation_files_percentage': 'Function Annotations',
    'kw_defaults_files_percentage': 'Keyword-only Arguments',
    'kw_args_files_percentage': 'Keyword-only Arguments',
    'type_vars_bounds_files_percentage': 'Type Parameter Syntax',
    'type_vars_constraints_files_percentage': 'Type Parameter Syntax',
    'type_param_spec_files_percentage': 'Type Parameter Syntax',
    'type_var_tuple_files_percentage': 'Type Parameter Syntax',
    'yield_from_files_percentage': 'Yield From Expression',
    'assignment_expression_files_percentage': 'Assignment Expression',
    'suppressing_exception_context_files_percentage': 'Suppressing Exception Context'
}

features_union_columns = {
    'Asynchronous Comprehensions',
    'Asynchronous Generators',
    'Matrix Multiplication',
    'Coroutines (async and await syntax)',
    'Formatted String Literals (f-strings)',
    'Exception Groups (except *)',
    'Structural Pattern Matching',
    'Extended Iterable Unpacking',
    'Additional Unpacking Generalizations',
    'Nonlocal Statements',
    'Function Annotations',
    'Keyword-only Arguments',
    'Type Parameter Syntax',
    'Yield From Expression',
    'Assignment Expression',
    'Suppressing Exception Context'
}

df_summary.rename(columns=features_mapping, inplace=True)

df_summary.to_csv('last_revision_files_occurrences_percentage.csv', index=False)

# Derreta o DataFrame para o formato apropriado
melted_df = pd.melt(df_summary, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Converta a coluna 'date' para datetime
melted_df['date'] = melted_df['date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce'))

# Converta a coluna 'value' para um tipo numérico
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

melted_df = melted_df.sort_values(by='date')

melted_df['feature'] = melted_df['feature'].replace(features_mapping)

summary = melted_df.groupby('feature')['total'].agg(['mean', 'median', 'std', 'max', 'min']).reset_index()

print(summary)
# exit()
# Calcular a média das porcentagens para cada feature por projeto
# project_feature_medians = df.groupby('project')[[feature + '_percentage' for feature in features_columns]].median().reset_index()

# print(project_feature_medians)
# sys.exit()

# Remover a coluna 'project' ao calcular a média geral

# print(df_last_revision)


df_last_revision.rename(columns=features_mapping, inplace=True)

df_last_revision = df_last_revision.groupby(df_last_revision.columns, axis=1).sum()

median_feature_usage = df_last_revision[[feature for feature in features_union_columns]].median().replace(features_mapping).reset_index()

# median_feature_usage['feature'] = median_feature_usage['feature']

median_feature_usage.columns = ['feature', 'median_percentage']


# median_feature_usage = median_feature_usage.groupby('feature')['median_percentage']
# print(median_feature_usage.head())
# sys.exit()

# print(median_feature_usage)
# sys.exit()

# Criar a tabela LaTeX
tablefmt = 'latex_booktabs'  # Formato LaTeX
colalign = ("right", "right")

table = tabulate(median_feature_usage.dropna().sort_values(by='median_percentage', ascending=False), 
                 headers=['Feature', 'median Usage (%)'], 
                 tablefmt=tablefmt, 
                 colalign=colalign)

print(table)

# Criar o gráfico boxplot
plt.figure(figsize=(10, 6))
sns.barplot(data=median_feature_usage.sort_values(by='median_percentage', ascending=False), x='median_percentage', y='feature', palette='viridis')
plt.title('median Usage of Features')
plt.xlabel('Median Percentage (%)')
plt.ylabel('Feature')
plt.grid(axis='x')
plt.tight_layout()

# Ajustar layout
plt.tight_layout()

# Salvar o gráfico em um arquivo PDF
with PdfPages('features_percentage_adoption_files_barplot.pdf') as pdf:
    pdf.savefig()
    
# Mostrar o gráfico
# plt.show()