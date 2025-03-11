import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess

df = pd.read_csv('results-without-gaps.csv')

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
    'type_alias',
    'yield_from',
    'assignment_expression',
    'suppressing_exception_context'
    ])

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

df['year_month'] = df['date'].dt.strftime('%Y-%m')

# Use a função groupby para agrupar o DataFrame por projeto e ano/mês
grouped = df.groupby(['project', 'year_month'])

# Encontre o índice da última revisão em cada grupo
last_revision_idx = grouped['date'].idxmax()

df_last_revision = df.loc[last_revision_idx]

# Defina as variáveis de interesse
# id_vars = ["project", "date", "year_month", "files", "statements"]
id_vars = ["project", "date", "year_month"]
value_name = "total"
var_name = "feature"

# Derreta o DataFrame para o formato apropriado
melted_df = pd.melt(df_last_revision, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Converta a coluna 'date' para datetime
melted_df['date'] = melted_df['date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce'))

melted_df['date'] = melted_df['year_month'].apply(lambda x: pd.to_datetime(x, format='%Y-%m', errors='coerce'))
# Converta a coluna 'value' para um tipo numérico
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')

melted_df = melted_df.sort_values(by='year_month')

# Lista de recursos (features)
features = [
    # 'async_list_comprehensions_files',
    # 'async_set_comprehensions_files',
    # 'async_dict_comprehensions_files',
    # 'async_generator_expressions_files',
    # 'matrix_multiplication_files',
    # 'async_def_files',
    # 'await_expressions_files',
    # 'async_for_files',
    # 'async_with_files',
    'fstring_files',
    # 'except_star_files',
    # 'pattern_match_files',
    # 'pattern_as_files',
    # 'pattern_or_files',
    # 'pattern_sequence_files',
    # 'pattern_mapping_files',
    # 'pattern_class_files',
    # 'pattern_value_files',
    # 'pattern_singleton_files',
    # 'pattern_star_files',
    # 'assign_unpack_files',
    # 'list_unpack_files',
    # 'tuple_unpack_files',
    # 'set_unpack_files',
    # 'dict_unpack_files',
    'call_kwargs_unpack_files',
    'call_args_unpack_files',
    # 'nonlocal_files',
    # 'function_args_annotation_files',
    # 'function_return_annotation_files',
    # 'kw_defaults_files',
    # 'kw_args_files',
    # 'type_vars_bounds_files',
    # 'type_vars_constraints_files',
    # 'type_param_spec_files',
    # 'type_var_tuple_files',
    # 'type_alias_files',
    # 'yield_from_files',
    # 'assignment_expression_files',
    # 'suppressing_exception_context_files'
]

plt.figure(figsize=(16, 8))

# Configurações do gráfico com seaborn
sns.set(style="whitegrid", font_scale=1.2)

# Iterar sobre os recursos e ajustar modelos de regressão e gerar gráficos
for feature in features:
    df_feature = melted_df[melted_df['feature'] == feature].copy()
    total_by_month = df_feature.groupby(['year_month'])['total'].sum().reset_index()

    X = sm.add_constant(total_by_month.index)  # Use o índice como variável independente
    y = total_by_month['total']  # Use a coluna 'total' como variável dependente

    # Aplicar a raiz quadrada a 'total'
    total_by_month['sqrt_total'] = np.sqrt(total_by_month['total'])

    # Criar as variáveis X e y com as colunas transformadas
    X_sqrt = sm.add_constant(total_by_month.index)
    y_sqrt = total_by_month['sqrt_total']
    
    
    # Cálculo da suavização loess
    loess_result = lowess(total_by_month['sqrt_total'], total_by_month.index, frac=0.25)
    total_by_month['loess'] = loess_result[:, 1]

    # Plotar a série temporal original normalizada
    # sns.lineplot(data=total_by_month, x='year_month', y='sqrt_total', label=f'{feature.replace("_", " ").title()} - Total Occurrences', errorbar=None, estimator=None, lw=2)

    # Calcular a tendência suavizada (loess) normalizada
    sns.lineplot(data=total_by_month, x='year_month', y='loess', label=f'{feature.replace("_", " ").title()}', errorbar=None, estimator=None, lw=2)

# Configurações do gráfico
plt.title('Smoothed Trends of Different Features')
plt.xlabel('Date (Year)')
plt.ylabel('Total Occurrences (#)')
plt.xticks(rotation=45)

x_ticks = np.arange(0, len(total_by_month), 12)  # Por exemplo, mostra um ponto a cada 12 meses
plt.xticks(x_ticks, total_by_month['year_month'].iloc[x_ticks].apply(lambda x: x[:4]), rotation=45)  # Exibe apenas o ano


plt.legend(fontsize='small')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Exibir o gráfico
plt.savefig('all_features_trends.pdf', bbox_inches='tight')  # Use bbox_inches='tight' para evitar que a legenda seja cortada