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

    fig = Figure(figsize=(5.88, 3.7), dpi=50)


    ax = fig.add_subplot(111)
    bars = ax.bar(contagem.index, contagem.values, color="#814BA8", edgecolor='black')
    ax.set_facecolor((0.29, 0.0, 0.51, 0.25))
    max_y = max(contagem.values)
    ax.set_ylim(0, max_y * 1.2)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')


    ax.set_title('Número de defeitos por categoria')
    ax.set_xlabel('Defeito')
    ax.set_ylabel('Quantidade')
    
    ax.set_xticks(range(len(contagem.index)))
    ax.set_xticklabels(contagem.index, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=master)
    return canvas