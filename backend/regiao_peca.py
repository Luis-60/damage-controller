from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def gerar_grafico_regiao_peca(df, master):
    # Preenchendo valores nulos para evitar erros
    df['PEÇA AFETADA'] = df['PEÇA AFETADA'].fillna('')
    df['REGIÃO'] = df['REGIÃO'].fillna('')

    # Filtrando linhas com valores não vazios em ambas as colunas
    mascara = (
        df['PEÇA AFETADA'].str.strip().ne('') &
        df['REGIÃO'].str.strip().ne('')
    )
    df_filtrado = df.loc[mascara].copy()

    # Agrupando e contando ocorrências
    lista_combinada = (
        df_filtrado
        .groupby(["PEÇA AFETADA", "REGIÃO"])
        .size()
        .reset_index(name='QTD')
        .sort_values(by='QTD', ascending=False)
    )

    # Criando labels para o eixo X com quebra de linha entre peça e região
    lista_combinada['LABEL'] = lista_combinada.apply(
        lambda row: f"{row['PEÇA AFETADA']}\n{row['REGIÃO']}", axis=1
    )

    # Pegando top 5
    lista_combinada = lista_combinada.head(5)

    rotulos = lista_combinada['LABEL'].tolist()
    valores = lista_combinada['QTD'].tolist()

    # Criando figura e eixo
    fig = Figure(figsize=(6.2, 4.6), dpi=50)
    ax = fig.add_subplot(111)

    if not valores:
        ax.text(0.5, 0.5, "Sem dados disponíveis",
                ha='center', va='center', fontsize=12, fontweight='bold')
        ax.axis('off')
        return FigureCanvasTkAgg(fig, master=master)

    bars = ax.bar(rotulos, valores, color="#814BA8", edgecolor='black')
    ax.set_facecolor((0.29, 0.0, 0.51, 0.25))
    ax.set_ylim(0, max(valores) * 1.2)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + max(valores)*0.05,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=11, fontweight='bold', color='black')

    ax.set_title('Regiões e Peças com Maior Número de Defeitos')
    ax.set_xlabel('Peça\nRegião')
    ax.set_ylabel('Quantidade')
    ax.set_xticks(range(len(rotulos)))
    ax.set_xticklabels(rotulos, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    fig.tight_layout()

    return FigureCanvasTkAgg(fig, master=master)
