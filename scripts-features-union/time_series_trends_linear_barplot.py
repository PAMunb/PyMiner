import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.nonparametric.smoothers_lowess import lowess
import statsmodels.api as sm
import seaborn as sns

# Lê o CSV
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
    'function_with_annotation','function_with_annotation_files',
    'function_without_annotation','function_without_annotation_files',
    'assign','assign_files','assign_with_type_comment','assign_with_type_comment_files',
    'aug_assign','aug_assign_files',
    'except_star',
    'except_star_with_group',
    'except_star_without_group',
    'raised_exception_group',
    'caught_exception_group',
    'exception_groups',
]
df = df.drop(columns=columns_to_drop)

# Converte data e cria coluna ano-mês
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
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
    'variable_annotation_files': 'Variable Annotation',
    'except_star_files': 'Except (*)',
    'exception_group_files': 'ExceptionGroup',
}
df.rename(columns=features_mapping, inplace=True)

# Agrupa por projeto e ano-mês, e pega última revisão de cada grupo
grouped = df.groupby(['project', 'year_month'])
last_revision_idx = grouped['date'].idxmax()
df_last = df.loc[last_revision_idx]

# Derrete o DataFrame para formato longo
id_vars = ["project", "date", "statements", "files", "year_month"]
melted_df = pd.melt(
    df_last,
    id_vars=id_vars,
    var_name='feature',
    value_name='total'
)

# Converte total para numérico e date para datetime ano-mês
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')
melted_df['date'] = pd.to_datetime(melted_df['year_month'], format='%Y-%m', errors='coerce')

# Lista fixa de features na ordem desejada
features = [
    'Asynchronous Comprehensions',
    'Asynchronous Generators',
    'Matrix Multiplication',
    'Coroutines (async and await syntax)',
    'Formatted String Literals (f-strings)',
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
    'Variable Annotation',
    'Except (*)',
    'ExceptionGroup',
]

# --- Geração do gráfico de barras com mês-ano mas exibindo só ano no eixo Y ---

# Filtra apenas onde houve uso (>0)
df_nonzero = melted_df[melted_df['total'] > 0].copy()

# Calcula a data (mês-ano) da primeira aparição de cada feature
first_dates = (
    df_nonzero
    .groupby('feature')['date']
    .min()
    .reindex(features)  # mantém ordem
)

# Converte para números de data do matplotlib
first_nums = mdates.date2num(first_dates.values)

# Plot
fig, ax = plt.subplots(figsize=(14, 6))
ax.bar(features, first_nums)

# Configurações de labels e título
ax.set_xlabel('Features')
ax.set_ylabel('Data de Primeira Ocorrência')
ax.set_title('Primeira Ocorrência de Cada Feature (Mês-Ano)')

# Rotaciona rótulos do eixo X
plt.xticks(rotation=90, ha='right')

# Formata eixo Y: apenas anos
ax.yaxis_date()
ax.yaxis.set_major_locator(mdates.YearLocator())         # um tick a cada ano
ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y')) # mostra só o ano
ax.yaxis.set_minor_locator(mdates.MonthLocator())        # ticks menores para meses (sem label)

plt.tight_layout()
plt.show()