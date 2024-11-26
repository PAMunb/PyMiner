import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
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

# Use a função groupby para agrupar o DataFrame por projeto e ano/mês
grouped = df.groupby(['project', 'year_month'])

# Encontre o índice da última revisão em cada grupo
last_revision_idx = grouped['date'].idxmax()

df_last_revision = df.loc[last_revision_idx]

# Defina as variáveis de interesse
id_vars = ["project", "date", "statements", "files", "year_month"]
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

# Função para ajustar modelos de regressão e gerar gráficos de tendência
def fit_and_plot_trends(df, feature, span):
    # Filtrar o DataFrame para o recurso específico
    df_feature = df[df['feature'] == feature].copy()

    total_by_month = df_feature.groupby(['feature', 'year_month'])['total'].sum().reset_index()

    df_feature = df_feature.merge(total_by_month, on='year_month', how='left')
    df_feature = df_feature.sort_values(by='year_month')

    # print(total_by_month)

    X = sm.add_constant(total_by_month['year_month'].index)  # Use o índice como variável independente
    y = total_by_month['total']  # Use a coluna 'total' como variável dependente

    # Aplicar a raiz quadrada a 'total'
    # total_by_month['sqrt_total'] = np.sqrt(total_by_month['total'])

    # Criar as variáveis X e y com as colunas transformadas
    X_sqrt = sm.add_constant(total_by_month['year_month'].index)
    y_sqrt = total_by_month['total']
    
    # Cálculo da suavização loess
    loess_result = lowess(total_by_month['total'], total_by_month['year_month'].index, frac=span)
    total_by_month['loess'] = loess_result[:, 1]

    # Encontrar o primeiro ponto de inclinação significativa
    # window_size = 12  # Tamanho da janela deslizante
    # slopes = []
    # for i in range(len(total_by_month) - window_size + 1):
    #     x_window = np.arange(i, i + window_size)  # Corrigir o eixo x
    #     y_window = total_by_month['loess'].iloc[i:i + window_size]

    #     # Ajustar um modelo de regressão linear
    #     slope, _ = np.polyfit(x_window, y_window, 1)
    #     slopes.append(slope)

    # # Encontrar o primeiro ponto de inclinação significativa
    # idx = np.argmax(slopes)
    # start_point = (total_by_month['year_month'].iloc[idx], total_by_month['loess'].iloc[idx])

    # Configurações do gráfico
    plt.figure(figsize=(12, 8))

    # Configurações do gráfico com seaborn
    sns.set(style="whitegrid", font_scale=1.2)

    # Plotar a série temporal original normalizada
    # sns.lineplot(data=total_by_month, x='year_month', y='sqrt_total', color='darkgray', label='Total Occurrences', errorbar=None, estimator=None, lw=2)

    # # Calcular a tendência suavizada (loess) normalizada
    sns.lineplot(data=total_by_month, x='year_month', y='loess', color='darkblue', errorbar=None, estimator=None, lw=2)

    # Configurações do gráfico
    plt.title(f'{feature.replace("_", " ").title()} Trend')
    plt.xlabel('Date (Year)')
    plt.ylabel('Total Occurrences (#)')
    plt.xticks(rotation=45)

    x_ticks = np.arange(0, len(total_by_month), 12)  # Por exemplo, mostra um ponto a cada 12 meses
    plt.xticks(x_ticks, total_by_month['year_month'].iloc[x_ticks].apply(lambda x: x[:4]), rotation=45)  # Exibe apenas o ano

    # # Adicionar a linha linear que indica o início da tendência
    # plt.axvline(x=start_point[0], color='red', linestyle='--', label='Trend Start')

    # Exibir o gráfico
    # plt.legend()
    plt.savefig(f'graphs/trend_{feature}.pdf')
    plt.close()

# Iterar sobre os recursos e ajustar modelos de regressão e gerar gráficos
for feature in features:
    fit_and_plot_trends(melted_df, feature, 0.25)
