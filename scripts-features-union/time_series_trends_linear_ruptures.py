import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess
import ruptures as rpt

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
    'function_with_annotation','function_with_annotation_files','function_without_annotation','function_without_annotation_files','assign','assign_files','assign_with_type_comment','assign_with_type_comment_files','aug_assign','aug_assign_files',
    'except_star',
    'except_star_with_group',
    'except_star_without_group',
    'raised_exception_group',
    'caught_exception_group',
    'exception_groups',
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

# Agrupar por projeto e ano/mês e pegar a última revisão de cada (para não duplicar o mesmo mês)
grouped = df.groupby(['project', 'year_month'])
last_revision_idx = grouped['date'].idxmax()
df_last_revision = df.loc[last_revision_idx]

# Variáveis de interesse
id_vars = ["project", "date", "statements", "files", "year_month"]
value_name = "total"
var_name = "feature"

# Derreter para long format
melted_df = pd.melt(df_last_revision, id_vars=id_vars, value_name=value_name, var_name=var_name)

# Forçar data como o começo do mês
melted_df['date'] = pd.to_datetime(melted_df['year_month'], format='%Y-%m', errors='coerce')
melted_df['total'] = pd.to_numeric(melted_df['total'], errors='coerce')
melted_df = melted_df.sort_values(by='year_month')

# Lista de features
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

# --- Utilitários para detecção de início de tendência ---

def detect_trend_start_from_loess(y_smooth, min_window=6, epsilon=0.05, max_bkps=5):
    """
    Detecta o primeiro ponto de mudança (ruptura) onde há aumento sustentado
    na média da série suavizada (LOESS).

    Parâmetros:
      - y_smooth: np.array 1D com a série suavizada
      - min_window: nº mínimo de meses para comparar as médias pré/pós
      - epsilon: limiar de crescimento relativo (5% por padrão)
      - max_bkps: número máximo de pontos de ruptura para procurar

    Retorna:
      - idx (int) do início da tendência (ou None se não encontrado)
    """
    n = len(y_smooth)
    if n < 2 * min_window:
        return None  # série muito curta

    # Ajustar modelo de mudanças de média (l2) com busca binária
    algo = rpt.Binseg(model="l2").fit(y_smooth)
    # limite prudente de breakpoints proporcional ao tamanho da série
    k = min(max_bkps, max(1, n // 24))
    bkps = algo.predict(n_bkps=k)  # índices são finais de segmentos (1..n)

    # Converter para índices de "início de segmento" candidatos
    # (primeiro breakpoint marca final do 1º segmento; idx candidato = bkp-1)
    for bkp in bkps:
        idx = max(1, min(n - 2, bkp - 1))  # garantir dentro do range

        # Checar janelas pré e pós
        pre_start = max(0, idx - min_window)
        pre_end = idx
        post_start = idx
        post_end = min(n, idx + min_window)

        pre_mean = np.mean(y_smooth[pre_start:pre_end]) if pre_end > pre_start else None
        post_mean = np.mean(y_smooth[post_start:post_end]) if post_end > post_start else None

        if pre_mean is None or post_mean is None:
            continue

        # Exigir crescimento relativo mínimo e valores não nulos
        if pre_mean >= 0 and post_mean > (pre_mean * (1 + epsilon)):
            return idx

    return None


# Lista para armazenar os resultados da detecção
trend_points = []

def fit_and_plot_trends(df, feature, span=0.2, outdir='graphs'):
    df_feature = df[df['feature'] == feature].copy()
    total_by_month = (
        df_feature.groupby(['feature', 'year_month'])['total']
        .sum().reset_index()
        .sort_values(by='year_month')
    )

    total_by_month = total_by_month.reset_index(drop=True)
    total_by_month['t_idx'] = np.arange(len(total_by_month))

    if len(total_by_month) == 0:
        return

    loess_result = lowess(
        endog=total_by_month['total'].values,
        exog=total_by_month['t_idx'].values,
        frac=span,
        return_sorted=False
    )
    total_by_month['loess'] = loess_result

    y_smooth = total_by_month['loess'].values.astype(float)
    trend_idx = detect_trend_start_from_loess(
        y_smooth,
        min_window=6,
        epsilon=0.05,
        max_bkps=5
    )

    # Salvar ponto encontrado para tabela
    if trend_idx is not None:
        ym = total_by_month.loc[trend_idx, 'year_month']
        value = total_by_month.loc[trend_idx, 'loess']
        trend_points.append({
            'feature': feature,
            'year_month': ym,
            'value': value
        })

    os.makedirs(outdir, exist_ok=True)
    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid", font_scale=1.2)
    sns.lineplot(data=total_by_month, x='t_idx', y='loess', lw=2, label='LOESS')

    x_ticks = np.arange(0, len(total_by_month), 12)
    plt.xticks(x_ticks, total_by_month['year_month'].iloc[x_ticks].str[:4], rotation=45)
    plt.title(f'{feature} — Trend')
    plt.xlabel('Year')
    plt.ylabel('Total Occurrences (#)')

    if trend_idx is not None:
        plt.axvline(x=trend_idx, color='red', linestyle='--', label='Trend start')
        plt.scatter([trend_idx], [y_smooth[trend_idx]], color='red', s=60, zorder=3)
        plt.annotate(f'{ym}', xy=(trend_idx, y_smooth[trend_idx]),
                     xytext=(trend_idx + 1, y_smooth[trend_idx]),
                     arrowprops=dict(arrowstyle='->', color='red'),
                     fontsize=10)

    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f'trend_{feature}.pdf'))
    plt.close()

# Executar para cada feature
for feature in features:
    fit_and_plot_trends(melted_df, feature, span=0.2, outdir='graphs')

# --- Gerar Tabela LaTeX ---
if trend_points:
    trend_df = pd.DataFrame(trend_points).sort_values(by='year_month')

    latex_table = "\\begin{table}[htb]\n\\centering\n"
    latex_table += "\\caption{Detected trend onset for each Python feature.}\n"
    latex_table += "\\label{tab:trend_onsets}\n"
    latex_table += "\\begin{tabular}{lcc}\n\\toprule\n"
    latex_table += "Feature & First Trend (Year-Month) & LOESS Value \\\\\n\\midrule\n"

    for _, row in trend_df.iterrows():
        latex_table += f"{row['feature']} & {row['year_month']} & {row['value']:.2f} \\\\\n"

    latex_table += "\\bottomrule\n\\end{tabular}\n\\end{table}\n"

    with open("trend_onsets_table.tex", "w") as f:
        f.write(latex_table)

    print("✅ Trend detection completed. Table saved to trend_onsets_table.tex")
else:
    print("⚠️ No trend points detected.")