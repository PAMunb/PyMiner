import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess

df = pd.read_csv('results-without-gaps.csv')

# Lista de colunas a serem removidas
columns_to_drop = [
    'commit_hash', 'errors',
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
    'variable_annotation'
]

df = df.drop(columns=columns_to_drop)


df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

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
# List of features
features = [
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
    'Suppressing Exception Context',
    'Variable Annotation'
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
    fit_and_plot_trends(melted_df, feature, 0.2)
