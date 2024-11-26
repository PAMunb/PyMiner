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

# Output folder for decomposition plots
output_folder = './decomposition'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Step 2: Decomposition
for feature in features:
    subset = melted_df[melted_df['feature'] == feature].copy()
    total_by_month = subset.groupby(['feature', 'date'])['total'].sum().reset_index()
    subset = subset.merge(total_by_month, on='date', how='left')
    subset = subset.sort_values(by='date')
    # total_by_month['sqrt_total'] = np.sqrt(total_by_month['total'])
    total_by_month = total_by_month.set_index('date')
    decomposition = seasonal_decompose(total_by_month['total'], model='additive', period=12)
    print(f'Decomposition of {feature}:')
    print(decomposition.trend.head())  # Print the first values of the trend
    print(decomposition.seasonal.head())  # Print the first values of the seasonal component
    print(decomposition.resid.head())  # Print the first values of the residuals
    pdf_filename = os.path.join(output_folder, f'decomposition_{feature}.pdf')
    decomposition.plot()
    plt.title(f'Decomposition of {feature}')
    plt.savefig(pdf_filename, format='pdf')

# Output folder for autocorrelation plots
output_folder = './auto-correlation'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Step 3: Autocorrelation
for feature in features:
    subset = melted_df[melted_df['feature'] == feature].copy()
    total_by_month = subset.groupby(['feature', 'date'])['total'].sum().reset_index()
    subset = subset.merge(total_by_month, on='date', how='left')
    subset = subset.sort_values(by='date')
    # total_by_month['sqrt_total'] = np.sqrt(total_by_month['total'])
    total_by_month = total_by_month.set_index('date')
    print(f'Autocorrelation Functions of {feature}:')
    plot_acf(total_by_month['total'], lags=50)
    plot_pacf(total_by_month['total'], lags=50)
    plt.title(f'Autocorrelation Functions of {feature}')
    pdf_filename = os.path.join(output_folder, f'auto_correlation_{feature}.pdf')
    plt.savefig(pdf_filename, format='pdf')

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