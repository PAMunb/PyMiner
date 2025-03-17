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
    'yield_from',
    'assignment_expression',
    'suppressing_exception_context',
    'variable_annotation',
    'function_with_annotation','function_with_annotation_files','function_without_annotation','function_without_annotation_files','assign','assign_files','assign_with_type_comment','assign_with_type_comment_files','aug_assign','aug_assign_files',
    ])

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Extract year and month from the 'date' column
df['year_month'] = df['date'].dt.strftime('%Y-%m')

# Dicionário de mapeamento de features
features_mapping = {
    'async_list_comprehensions_files': 'Asynchronous Comprehensions',
    'async_set_comprehensions_files': 'Asynchronous Comprehensions',
    'async_dict_comprehensions_files': 'Asynchronous Comprehensions',
    'async_generator_expressions_files': 'Asynchronous Generators',
    'matrix_multiplication_files': 'Matrix Multiplication',
    'async_def_files': 'Coroutines (async and await syntax)',
    'await_expressions_files': 'Coroutines (async and await syntax)',
    'async_for_files': 'Coroutines (async and await syntax)',
    'async_with_files': 'Coroutines (async and await syntax)',
    'fstring_files': 'Formatted String Literals (f-strings)',
    'except_star_files': 'Exception Groups (except *)',
    'pattern_match_files': 'Structural Pattern Matching',
    'pattern_as_files': 'Structural Pattern Matching',
    'pattern_or_files': 'Structural Pattern Matching',
    'pattern_sequence_files': 'Structural Pattern Matching',
    'pattern_mapping_files': 'Structural Pattern Matching',
    'pattern_class_files': 'Structural Pattern Matching',
    'pattern_value_files': 'Structural Pattern Matching',
    'pattern_singleton_files': 'Structural Pattern Matching',
    'pattern_star_files': 'Structural Pattern Matching',
    'assign_unpack_files': 'Extended Iterable Unpacking',
    'list_unpack_files': 'Additional Unpacking Generalizations',
    'tuple_unpack_files': 'Additional Unpacking Generalizations',
    'set_unpack_files': 'Additional Unpacking Generalizations',
    'dict_unpack_files': 'Additional Unpacking Generalizations',
    'call_kwargs_unpack_files': 'Additional Unpacking Generalizations',
    'call_args_unpack_files': 'Additional Unpacking Generalizations',
    'nonlocal_files': 'Nonlocal Statements',
    'function_args_annotation_files': 'Function Annotations',
    'function_return_annotation_files': 'Function Annotations',
    'kw_defaults_files': 'Keyword-only Arguments',
    'kw_args_files': 'Keyword-only Arguments',
    'type_vars_bounds_files': 'Type Parameter Syntax',
    'type_vars_constraints_files': 'Type Parameter Syntax',
    'type_param_spec_files': 'Type Parameter Syntax',
    'type_var_tuple_files': 'Type Parameter Syntax',
    'yield_from_files': 'Yield From Expression',
    'assignment_expression_files': 'Assignment Expression',
    'suppressing_exception_context_files': 'Suppressing Exception Context',
    'variable_annotation_files': 'Variable Annotation'
}


df.rename(columns=features_mapping, inplace=True)

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
features = [
    'Asynchronous Comprehensions',
    # 'Asynchronous Generators',
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
    'Suppressing Exception Context',
    'Variable Annotation'
]

# # Output folder for decomposition plots
# output_folder = './decomposition'
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # Step 2: Decomposition
# for feature in features:
#     subset = melted_df[melted_df['feature'] == feature].copy()
#     total_by_month = subset.groupby(['feature', 'date'])['total'].sum().reset_index()
#     subset = subset.merge(total_by_month, on='date', how='left')
#     subset = subset.sort_values(by='date')
#     # total_by_month['sqrt_total'] = np.sqrt(total_by_month['total'])
#     total_by_month = total_by_month.set_index('date')
#     decomposition = seasonal_decompose(total_by_month['total'], model='additive', period=12)
#     print(f'Decomposition of {feature}:')
#     print(decomposition.trend.head())  # Print the first values of the trend
#     print(decomposition.seasonal.head())  # Print the first values of the seasonal component
#     print(decomposition.resid.head())  # Print the first values of the residuals
#     pdf_filename = os.path.join(output_folder, f'decomposition_{feature}.pdf')
#     decomposition.plot()
#     plt.title(f'Decomposition of {feature}')
#     plt.savefig(pdf_filename, format='pdf')

# # Output folder for autocorrelation plots
# output_folder = './auto-correlation'
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # Step 3: Autocorrelation
# for feature in features:
#     subset = melted_df[melted_df['feature'] == feature].copy()
#     total_by_month = subset.groupby(['feature', 'date'])['total'].sum().reset_index()
#     subset = subset.merge(total_by_month, on='date', how='left')
#     subset = subset.sort_values(by='date')
#     # total_by_month['sqrt_total'] = np.sqrt(total_by_month['total'])
#     total_by_month = total_by_month.set_index('date')
#     print(f'Autocorrelation Functions of {feature}:')
#     plot_acf(total_by_month['total'], lags=50)
#     plot_pacf(total_by_month['total'], lags=50)
#     plt.title(f'Autocorrelation Functions of {feature}')
#     pdf_filename = os.path.join(output_folder, f'auto_correlation_{feature}.pdf')
#     plt.savefig(pdf_filename, format='pdf')

# Step 5: Augmented Dickey-Fuller (ADF) Test for Stationarity
for feature in features:
    subset = melted_df[melted_df['feature'] == feature].copy()
    total_by_month = subset.groupby(['feature', 'date'])['total'].sum().reset_index()
    subset = subset.merge(total_by_month, on='date', how='left')
    subset = subset.sort_values(by='date')
    # total_by_month['sqrt_total'] = np.sqrt(total_by_month['total'])
    total_by_month = total_by_month.set_index('date')
    result = adfuller(total_by_month['total'])
    print(f'ADF Test for {feature}:')
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:', result[4])
    print('Test Results:')
    if result[1] <= 0.05:
        print('The series is stationary (rejects the null hypothesis)')
    else:
        print('The series is non-stationary (fails to reject the null hypothesis)')
    print('-' * 40)

# Step 6: Kendall Coefficient and p-value Test to evaluate trend direction
for feature in features:
    subset = melted_df[melted_df['feature'] == feature].copy()
    total_by_month = subset.groupby(['feature', 'date'])['total'].sum().reset_index()
    subset = subset.merge(total_by_month, on='date', how='left')
    subset = subset.sort_values(by='date')
    # total_by_month['sqrt_total'] = np.sqrt(total_by_month['total'])
    total_by_month = total_by_month.set_index('date')
    # Calculate Kendall coefficient and p-value
    coeficient_kendall, p_value = kendalltau(total_by_month['total'], total_by_month.index)
    # Check if the p-value is less than the significance level (e.g., 0.05)
    significance_level = 0.05
    print('Kendall Coefficient:', coeficient_kendall)
    print(f'p-value: {p_value:.25f}')
    print('Significance Level:', significance_level)
    if coeficient_kendall > 0:
        print(f'Increasing Trend in the Time Series for {feature}.')
    elif coeficient_kendall < 0:
        print(f'Decreasing Trend in the Time Series for {feature}.')
    else:
        print(f'No Significant Trend in the Time Series for {feature}.')