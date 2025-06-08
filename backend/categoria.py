from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def gerar_grafico_categoria(lista, master):
    lista['DEFEITOS'] = lista['DEFEITOS'].fillna('')

    mascara = (
        lista['DEFEITOS'].str.strip().ne('')  # não-vazio
        & lista['DEFEITOS'].str.strip().str.upper().ne('O SEM DEFEITO')
    )

    lista_filtrada = lista.loc[mascara].copy()

    contagem = lista_filtrada['DEFEITOS'].value_counts().head(5)

    fig = Figure(figsize=(3.3, 2.5), dpi=100)
    ax = fig.add_subplot(111)
    bars = ax.bar(contagem.index, contagem.values, color='lightblue', edgecolor='black')


    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(height)}',
                ha='center', va='bottom', fontsize=9)


    ax.set_title('Número de defeitos por categoria')
    ax.set_xlabel('Defeito')
    ax.set_ylabel('Quantidade')
    ax.set_xticks(axis='x', which='major', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    canvas = FigureCanvasTkAgg(fig, master=master)
    return canvas