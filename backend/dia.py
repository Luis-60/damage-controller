from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def gerar_grafico_por_dia(df, master):
    df['DEFEITOS'] = df['DEFEITOS'].fillna('')
    df['DATA'] = df['DATA'].fillna('')
    df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')

    df_filtrado = df[
        (df['DEFEITOS'].str.strip() != '') &
        (df['DEFEITOS'].str.strip().str.upper() != 'O SEM DEFEITO') &
        (df['DATA'].notna())
    ]


    df_filtrado = df[df['DEFEITOS'].notna()].copy()
    df_filtrado.loc[:, 'DIA'] = df_filtrado['DATA'].dt.day



    contagem = df_filtrado['DIA'].value_counts().sort_index()

    if contagem.empty:
        fig = Figure(figsize=(6.5, 3.7), dpi=50)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "Sem dados disponíveis",
                ha='center', va='center', fontsize=10, fontweight='bold')
        ax.axis('off')
        return FigureCanvasTkAgg(fig, master=master)

    categorias = contagem.index.astype(str)
    valores = contagem.values

    fig = Figure(figsize=(5.88, 3.7), dpi=50)
    ax = fig.add_subplot(111)

    bars = ax.bar(categorias, valores, color="#814BA8", edgecolor='black')
    ax.set_facecolor((0.29, 0.0, 0.51, 0.25))
    ax.set_ylim(0, max(valores) * 1.2)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='black', rotation=90, 
                bbox=dict(facecolor='#E5BEEC', edgecolor='black', boxstyle='round,pad=0.2')
                )

    ax.set_title('Quantidade de Defeitos por Dia')
    ax.set_xlabel('Dia do Mês')
    ax.set_ylabel('Número de Defeitos')
    ax.set_xticks(range(len(categorias)))
    ax.set_xticklabels(categorias, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()

    return FigureCanvasTkAgg(fig, master=master)
