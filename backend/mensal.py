from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
import pandas as pd

def gerar_grafico_mensal(df, master):
    df['DEFEITOS'] = df['DEFEITOS'].fillna('')
    df['DATA'] = df['DATA'].fillna('')
    df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')

    df_filtrado = df[
        (df['DEFEITOS'].str.strip() != '') &
        (df['DEFEITOS'].str.strip().str.upper() != 'O SEM DEFEITO') &
        (df['DATA'].notna())
    ]

    df_filtrado['MES'] = df_filtrado['DATA'].dt.month

    contagem = df_filtrado['MES'].value_counts().sort_index()

    categorias = [calendar.month_name[mes].capitalize() for mes in contagem.index]
    valores = contagem.values

    fig = Figure(figsize=(3.3, 2.5), dpi=100)
    ax = fig.add_subplot(111)
    bars = ax.bar(categorias, valores, color='lightblue', edgecolor='black',width=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(height)}',
                ha='center', va='bottom', fontsize=9)

    ax.set_title('Quantidade de Defeitos por Mês')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Número de Defeitos')
    ax.tick_params(axis='x', which='major', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    canvas = FigureCanvasTkAgg(fig, master=master)
    return canvas