import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess

df = pd.read_csv('~/Documents/JSMiner/scripts/results-without-gaps.csv')

df = df.drop(columns=['revision', 'errors','async_declarations_files','await_declarations_files','const_declarations_files','class_declarations_files',
'arrow_function_declarations_files','let_declarations_files','export_declarations_files','yield_declarations_files',
'import_statements_files','default_parameters_files',
'rest_statements_files','spread_arguments_files','array_destructuring_files','object_destructuring_files',
'optional_chain_files','template_string_expressions_files','null_coalesce_operators_files','exponentiation_assignments_files','private_fields_files',
'numeric_separator_files','big_int_files','enhanced_property_assignment_files','computed_property_assignment_files','function_property_declaration_files'])

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
    'async_declarations',
    # 'await_declarations',
    # 'files',
    # 'statements',
    'const_declarations',
    # 'class_declarations',
    'arrow_function_declarations',
    # 'let_declarations',
    # 'export_declarations',
    # 'yield_declarations',
    # 'import_statements',
    # 'default_parameters',
    # 'rest_statements',
    # 'spread_arguments',
    # 'array_destructuring',
    # 'object_destructuring',
    # 'yield_declarations',
    # 'optional_chain',
    # 'template_string_expressions',
    # 'null_coalesce_operators',
    # 'private_fields',
    # 'numeric_separator',
    # 'enhanced_property_assignment',
    # 'computed_property_assignment',
    # 'function_property_declaration'
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