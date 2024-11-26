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
    'dict_union_files', 'dict_union_update_files',
    'async_list_comprehensions_files', 'async_set_comprehensions_files', 'async_dict_comprehensions_files', 
    'async_generator_expressions_files', 'matrix_multiplication_files',
    'async_def_files', 'await_expressions_files', 'async_for_files', 'async_with_files',
    'fstring_files', 'except_star_files', 
    'structural_pattern_match_files', 'pattern_as_files', 'pattern_or_files', 'pattern_sequence_files',
    'pattern_mapping_files', 'pattern_class_files', 'pattern_value_files', 'pattern_singleton_files', 
    'pattern_star_files', 'assign_unpack_files', 'list_unpack_files', 'tuple_unpack_files', 'set_unpack_files', 
    'dict_unpack_files', 'call_kwargs_unpack_files', 'call_args_unpack_files', 
    'nonlocal_files', 'function_args_annotation_files', 'function_return_annotation_files', 
    'kw_defaults_files', 'kw_args_files', 
    'type_vars_bounds_files', 'type_vars_constraints_files', 'type_param_spec_files', 'type_var_tuple_files', 
    'type_alias_files', 'type_hint_list_files', 'type_hint_tuple_files', 'type_hint_dict_files', 
    'type_hint_set_files', 'type_hint_frozenset_files', 'type_hint_type_files'
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

df_summary = df_last_revision.drop(columns=['dict_union', 'dict_union_update',
    'async_list_comprehensions', 'async_set_comprehensions', 'async_dict_comprehensions', 
    'async_generator_expressions', 'matrix_multiplication',
    'async_def', 'await_expressions', 'async_for', 'async_with',
    'fstring', 'except_star', 
    'structural_pattern_match', 'pattern_as', 'pattern_or', 'pattern_sequence',
    'pattern_mapping', 'pattern_class', 'pattern_value', 'pattern_singleton', 
    'pattern_star', 'assign_unpack', 'list_unpack', 'tuple_unpack', 'set_unpack', 
    'dict_unpack', 'call_kwargs_unpack', 'call_args_unpack', 
    'nonlocal', 'function_args_annotation', 'function_return_annotation', 
    'kw_defaults', 'kw_args', 
    'type_vars_bounds', 'type_vars_constraints', 'type_param_spec', 'type_var_tuple', 
    'type_alias', 'type_hint_list', 'type_hint_tuple', 'type_hint_dict', 
    'type_hint_set', 'type_hint_frozenset', 'type_hint_type'])

df_summary = df_summary.drop(columns=['errors', 'dict_union_files', 'dict_union_update_files',
    'async_list_comprehensions_files', 'async_set_comprehensions_files', 'async_dict_comprehensions_files', 
    'async_generator_expressions_files', 'matrix_multiplication_files',
    'async_def_files', 'await_expressions_files', 'async_for_files', 'async_with_files',
    'fstring_files', 'except_star_files', 
    'structural_pattern_match_files', 'pattern_as_files', 'pattern_or_files', 'pattern_sequence_files',
    'pattern_mapping_files', 'pattern_class_files', 'pattern_value_files', 'pattern_singleton_files', 
    'pattern_star_files', 'assign_unpack_files', 'list_unpack_files', 'tuple_unpack_files', 'set_unpack_files', 
    'dict_unpack_files', 'call_kwargs_unpack_files', 'call_args_unpack_files', 
    'nonlocal_files', 'function_args_annotation_files', 'function_return_annotation_files', 
    'kw_defaults_files', 'kw_args_files', 
    'type_vars_bounds_files', 'type_vars_constraints_files', 'type_param_spec_files', 'type_var_tuple_files', 
    'type_alias_files', 'type_hint_list_files', 'type_hint_tuple_files', 'type_hint_dict_files', 
    'type_hint_set_files', 'type_hint_frozenset_files', 'type_hint_type_files'])

df_summary.to_csv('last_revision_files_occurrences_percentage.csv', index=False)

# Derreta o DataFrame para o formato apropriado
melted_df = pd.melt(df_summary, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Converta a coluna 'date' para datetime
melted_df['date'] = melted_df['date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce'))

# Converta a coluna 'value' para um tipo numérico
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

melted_df = melted_df.sort_values(by='date')

summary = melted_df.groupby('feature')['total'].agg(['median', 'mean', 'std', 'max', 'min']).reset_index()
# print(summary)
# exit()
# Calcular a média das porcentagens para cada feature por projeto
# project_feature_means = df.groupby('project')[[feature + '_percentage' for feature in features_columns]].mean().reset_index()

# print(project_feature_means)
# sys.exit()

# Remover a coluna 'project' ao calcular a média geral
mean_feature_usage = df_last_revision[[feature + '_percentage' for feature in features_columns]].mean().reset_index()
mean_feature_usage.columns = ['feature', 'mean_percentage']

# print(mean_feature_usage)
# sys.exit()

# Dicionário de mapeamento de features
features_mapping = {
    'dict_union_files_percentage': 'Dictionary Union',
    'dict_union_update_files_percentage': 'Dictionary Union Update',
    'async_list_comprehensions_files_percentage': 'Async List Comprehensions',
    'async_set_comprehensions_files_percentage': 'Async Set Comprehensions',
    'async_dict_comprehensions_files_percentage': 'Async Dictionary Comprehensions',
    'async_generator_expressions_files_percentage': 'Async Generator Expressions',
    'matrix_multiplication_files_percentage': 'Matrix Multiplication',
    'async_def_files_percentage': 'Async Function Definitions',
    'await_expressions_files_percentage': 'Await Expressions',
    'async_for_files_percentage': 'Async For Loops',
    'async_with_files_percentage': 'Async With Statements',
    'fstring_files_percentage': 'Formatted String Literals (f-strings)',
    'except_star_files_percentage': 'Exception Groups (except *)',
    'structural_pattern_match_files_percentage': 'Structural Pattern Matching',
    'pattern_as_files_percentage': 'Pattern As Bindings',
    'pattern_or_files_percentage': 'Pattern Or',
    'pattern_sequence_files_percentage': 'Pattern Sequence',
    'pattern_mapping_files_percentage': 'Pattern Mapping',
    'pattern_class_files_percentage': 'Pattern Class',
    'pattern_value_files_percentage': 'Pattern Value',
    'pattern_singleton_files_percentage': 'Pattern Singleton',
    'pattern_star_files_percentage': 'Pattern Star',
    'assign_unpack_files_percentage': 'Assignment Unpacking',
    'list_unpack_files_percentage': 'List Unpacking',
    'tuple_unpack_files_percentage': 'Tuple Unpacking',
    'set_unpack_files_percentage': 'Set Unpacking',
    'dict_unpack_files_percentage': 'Dictionary Unpacking',
    'call_kwargs_unpack_files_percentage': 'Call Keyword Arguments Unpacking',
    'call_args_unpack_files_percentage': 'Call Positional Arguments Unpacking',
    'nonlocal_files_percentage': 'Nonlocal Statements',
    'function_args_annotation_files_percentage': 'Function Argument Annotations',
    'function_return_annotation_files_percentage': 'Function Return Annotations',
    'kw_defaults_files_percentage': 'Keyword Defaults',
    'kw_args_files_percentage': 'Keyword Arguments',
    'type_vars_bounds_files_percentage': 'Type Variables Bounds',
    'type_vars_constraints_files_percentage': 'Type Variables Constraints',
    'type_param_spec_files_percentage': 'Type Parameter Specification',
    'type_var_tuple_files_percentage': 'Type Variable Tuple',
    'type_alias_files_percentage': 'Type Aliases',
    'type_hint_list_files_percentage': 'Type Hint for Lists',
    'type_hint_tuple_files_percentage': 'Type Hint for Tuples',
    'type_hint_dict_files_percentage': 'Type Hint for Dictionaries',
    'type_hint_set_files_percentage': 'Type Hint for Sets',
    'type_hint_frozenset_files_percentage': 'Type Hint for Frozen Sets',
    'type_hint_type_files_percentage': 'Type Hint for Types'
}

mean_feature_usage['feature'] = mean_feature_usage['feature'].map(features_mapping)

# print(mean_feature_usage)
# sys.exit()

# Criar a tabela LaTeX
tablefmt = 'latex_booktabs'  # Formato LaTeX
colalign = ("right", "right")

table = tabulate(mean_feature_usage.dropna().sort_values(by='mean_percentage', ascending=False), 
                 headers=['Feature', 'Mean Usage (%)'], 
                 tablefmt=tablefmt, 
                 colalign=colalign)

print(table)

# Criar o gráfico boxplot
plt.figure(figsize=(10, 6))
sns.barplot(data=mean_feature_usage.sort_values(by='mean_percentage', ascending=False), x='mean_percentage', y='feature', palette='viridis')
plt.title('Mean Usage of Features')
plt.xlabel('Mean Percentage (%)')
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