from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def gerar_grafico_responsavel(df, master):
    df['RESPONSÁVEL'] = df['RESPONSÁVEL'].fillna('')
    df['DEFEITOS'] = df['DEFEITOS'].fillna('')

    df_filtrado = df[
        (df['DEFEITOS'].str.strip() != '') &
        (df['DEFEITOS'].str.strip().str.upper() != 'O SEM DEFEITO')
    ]

    contagem = df_filtrado['RESPONSÁVEL'].value_counts().head(5)

    fig = Figure(figsize=(3.3, 2.5), dpi=100)
    ax = fig.add_subplot(111)

    bars = ax.bar(contagem.index, contagem.values, color='lightblue', edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(height)}',
                ha='center', va='bottom', fontsize=9)

    ax.set_title('Quantidade de Defeitos por Responsável')
    ax.set_xlabel('Responsável')
    ax.set_ylabel('Número de Defeitos')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    canvas = FigureCanvasTkAgg(fig, master=master)
    return canvas
