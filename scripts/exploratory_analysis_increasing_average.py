import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from scipy.stats import kendalltau
import os

# Read the CSV file into a DataFrame
df = pd.read_csv('results-without-gaps.csv')

# Drop unnecessary columns
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

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Extract year and month from the 'date' column
df['year_month'] = df['date'].dt.strftime('%Y-%m')

# Group the DataFrame by project and year/month
grouped = df.groupby(['project', 'year_month'])

# Find the index of the last revision in each group
last_revision_idx = grouped['date'].idxmax()

# Get the rows corresponding to the last revision in each group
df_last_revision = df.loc[last_revision_idx]

# Define variables of interest
id_vars = ["project", "date", "statements", "files", "year_month"]
value_name = "total"
var_name = "feature"

# Melt the DataFrame to the appropriate format
melted_df = pd.melt(df_last_revision, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Convert the 'date' column to datetime format
melted_df['date'] = melted_df['date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce'))

# Convert the 'year_month' column to datetime format
melted_df['date'] = melted_df['year_month'].apply(lambda x: pd.to_datetime(x, format='%Y-%m', errors='coerce'))

# Convert the 'total' column to numeric
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

# Sort the DataFrame by 'year_month'
melted_df = melted_df.sort_values(by='year_month')

# List of features
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
    'type_hint_type': 'Type Hint for Types'
}

for feature in features_mapping:
    subset = melted_df[melted_df['feature'] == feature].copy()

    total_by_month = subset.groupby(['feature', 'year_month'])['total'].sum().reset_index()

    # 1. Calcular a diferença entre os totais de ocorrências em cada mês e o mês anterior para cada feature
    total_by_month['diff'] = total_by_month['total'].diff()

    # 2. Calcular a média dessas diferenças para cada feature
    average_difference_per_feature = total_by_month['diff'].mean()

    # Exibir os resultados
    print(feature,average_difference_per_feature)


