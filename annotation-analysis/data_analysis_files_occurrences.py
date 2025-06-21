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
    'assignment_expression_files',
    'variable_annotation_files',
    'function_with_annotation_files','function_without_annotation_files','assign_files','assign_with_type_comment_files','aug_assign_files',
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
    'yield_from',
    'variable_annotation',
    'assignment_expression',
    'suppressing_exception_context',
    'function_with_annotation','function_with_annotation_files','function_without_annotation','function_without_annotation_files','assign','assign_files','assign_with_type_comment','assign_with_type_comment_files','aug_assign','aug_assign_files',
	'except_star',
	'except_star_with_group',
	'except_star_without_group',
	'raised_exception_group',
	'caught_exception_group',
	'exception_groups',
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
    'variable_annotation_files',
    'suppressing_exception_context_files',
	'except_star_files',
	'exception_group_files'
    ])

df_summary.to_csv('last_revision_files_occurrences_percentage.csv', index=False)

# Derreta o DataFrame para o formato apropriado
melted_df = pd.melt(df_summary, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Converta a coluna 'date' para datetime
melted_df['date'] = melted_df['date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce'))

# Converta a coluna 'value' para um tipo numérico
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

melted_df = melted_df.sort_values(by='date')

# Dicionário de mapeamento de features
features_mapping = {
        'function_with_annotation_files_percentage': 'Function With Annotations',
        'function_without_annotation_files_percentage': 'Traditional Functions',
        'assignment_expression_files_percentage': 'Assignment Expression',
        'variable_annotation_files_percentage': 'Variable Annotation',
        'assign_files_percentage': 'Assign',
        'assign_with_type_comment_files_percentage': 'Assign With Type Comment',
        'aug_assign_files_percentage': 'AugAssign',
}

summary = melted_df.groupby('feature')['total'].agg(['mean', 'median', 'std', 'max', 'min']).reset_index()

summary['feature'] = summary['feature'].replace(features_mapping)

print(summary)
# exit()
# Calcular a média das porcentagens para cada feature por projeto
# project_feature_medians = df.groupby('project')[[feature + '_percentage' for feature in features_columns]].median().reset_index()

# print(project_feature_medians)
# sys.exit()

# Remover a coluna 'project' ao calcular a média geral
median_feature_usage = df_last_revision[[feature + '_percentage' for feature in features_columns]].median().reset_index()
median_feature_usage.columns = ['feature', 'median_percentage']

# print(median_feature_usage)
# sys.exit()

median_feature_usage['feature'] = median_feature_usage['feature'].map(features_mapping)

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