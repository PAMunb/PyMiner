import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess

df = pd.read_csv('results-without-gaps.csv')

df = df.drop(columns=['commit_hash', 'errors',
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
    'type_hint_set_files', 'type_hint_frozenset_files', 'type_hint_type_files'])

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

df['year_month'] = df['date'].dt.strftime('%Y-%m')

# Group DataFrame by project and year/month
grouped = df.groupby(['project', 'year_month'])

# Find the index of the last revision in each group
last_revision_idx = grouped['date'].idxmax()

df_last_revision = df.loc[last_revision_idx]

# Define variables of interest
id_vars = ["project", "date", "statements", "files", "year_month"]
value_name = "total"
var_name = "feature"

# Melt the DataFrame into the appropriate format
melted_df = pd.melt(df_last_revision, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Convert the 'date' column to datetime
melted_df['date'] = pd.to_datetime(melted_df['date'], format='%Y-%m-%d', errors='coerce')

# Convert the 'year_month' column to datetime
melted_df['year_month'] = pd.to_datetime(melted_df['year_month'], format='%Y-%m', errors='coerce')

# Convert the 'total' column to numeric
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

melted_df = melted_df.sort_values(by='year_month')

# List of features
features = [
'dict_union', 'dict_union_update',
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
    'type_hint_set', 'type_hint_frozenset', 'type_hint_type'
]

# Calculate the correlation among selected features, files, and statements
correlation_df = melted_df.pivot_table(index='year_month', columns='feature', values='total', aggfunc='sum')
correlation_df = correlation_df[features]  # Select only the features from the list
correlation_df['files'] = melted_df.groupby('year_month')['files'].mean()
correlation_df['statements'] = melted_df.groupby('year_month')['statements'].mean()
correlation_matrix = correlation_df.corr()

# Scale down the numbers in the correlation matrix
correlation_matrix = correlation_matrix.round(2)
# correlation_matrix_filtered = correlation_matrix[correlation_matrix > 0.6]

# Dicionário de mapeamento de features
features_mapping = {
    'dict_union': 'Dictionary Union',
    'dict_union_update': 'Dictionary Union Update',
    'async_list_comprehensions': 'Async List Comprehensions',
    'async_set_comprehensions': 'Async Set Comprehensions',
    'async_dict_comprehensions': 'Async Dictionary Comprehensions',
    'async_generator_expressions': 'Async Generator Expressions',
    'matrix_multiplication': 'Matrix Multiplication',
    'async_def': 'Async Function Definitions',
    'await_expressions': 'Await Expressions',
    'async_for': 'Async For Loops',
    'async_with': 'Async With Statements',
    'fstring': 'Formatted String Literals (f-strings)',
    'except_star': 'Exception Groups (except *)',
    'structural_pattern_match': 'Structural Pattern Matching',
    'pattern_as': 'Pattern As Bindings',
    'pattern_or': 'Pattern Or',
    'pattern_sequence': 'Pattern Sequence',
    'pattern_mapping': 'Pattern Mapping',
    'pattern_class': 'Pattern Class',
    'pattern_value': 'Pattern Value',
    'pattern_singleton': 'Pattern Singleton',
    'pattern_star': 'Pattern Star',
    'assign_unpack': 'Assignment Unpacking',
    'list_unpack': 'List Unpacking',
    'tuple_unpack': 'Tuple Unpacking',
    'set_unpack': 'Set Unpacking',
    'dict_unpack': 'Dictionary Unpacking',
    'call_kwargs_unpack': 'Call Keyword Arguments Unpacking',
    'call_args_unpack': 'Call Positional Arguments Unpacking',
    'nonlocal': 'Nonlocal Statements',
    'function_args_annotation': 'Function Argument Annotations',
    'function_return_annotation': 'Function Return Annotations',
    'kw_defaults': 'Keyword Defaults',
    'kw_args': 'Keyword Arguments',
    'type_vars_bounds': 'Type Variables Bounds',
    'type_vars_constraints': 'Type Variables Constraints',
    'type_param_spec': 'Type Parameter Specification',
    'type_var_tuple': 'Type Variable Tuple',
    'type_alias': 'Type Aliases',
    'type_hint_list': 'Type Hint for Lists',
    'type_hint_tuple': 'Type Hint for Tuples',
    'type_hint_dict': 'Type Hint for Dictionaries',
    'type_hint_set': 'Type Hint for Sets',
    'type_hint_frozenset': 'Type Hint for Frozen Sets',
    'type_hint_type': 'Type Hint for Types',
    'files': 'Files',
    'statements': 'Statements'
}


feature_names = [features_mapping[feature] for feature in correlation_matrix.columns]
# Plot the correlation matrix
plt.figure(figsize=(16, 14))
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar=True, square=True, annot_kws={"size": 8})
plt.title('Correlation Matrix')

# Mapeando os nomes das features para os y-labels
feature_names_y = [features_mapping[feature] for feature in correlation_matrix.index if feature in features_mapping]

heatmap.set_xticklabels(feature_names, rotation=45, ha='right')
heatmap.set_yticklabels(feature_names)

# Adicionando margens e centralizando a figura
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

# Ajustando o retângulo de layout para aumentar o tamanho dentro do PDF
plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])

# Salvar a tabela de correlação em LaTeX
correlation_latex = correlation_matrix.to_latex(float_format="%.2f")
with open("correlation_matrix.tex", "w") as text_file:
    text_file.write(correlation_latex)

# Salvar o gráfico em PDF
pdf_filename = os.path.join(f'features_correlation.pdf')
plt.savefig(pdf_filename, format='pdf')