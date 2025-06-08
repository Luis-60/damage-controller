from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def gerar_grafico_turno(lista, master):
    lista['TURNO'] = lista['TURNO'].fillna('')
    lista['TURNO'] = lista['TURNO'].str.replace(r"[\r\n]", "", regex=True)

    mascara = (
        lista['TURNO'].str.strip().ne('')  # não-vazio
    )

    lista_filtrada = lista.loc[mascara].copy()

    # Mapeamento das variações
    mapeamento_regex = {
        "Shift #1": "1º TURNO",
        "Shift #2": "2º TURNO",
        "1T": "1º TURNO",
        "2T": "2º TURNO",
        "1º TURNO": "1º TURNO",
        "2º TURNO": "2º TURNO",
    }

    # Normalizar os valores
    lista_filtrada['TURNO_NORMALIZADO'] = lista_filtrada['TURNO'].map(lambda x: mapeamento_regex.get(x, x))

    contagem_turnos = lista_filtrada['TURNO_NORMALIZADO'].value_counts()

    fig = Figure(figsize=(5.1, 4.58), dpi=50)
    ax = fig.add_subplot(111)
    
    # Cor padrão: roxo (claro e escuro alternando para contraste, se necessário)
    cores = ['#814BA8', '#A678C7'] if len(contagem_turnos) == 2 else ['#814BA8'] * len(contagem_turnos)

    # Gráfico com padrão de cores
    wedges, texts, autotexts = ax.pie(
        x=contagem_turnos.values,
        labels=contagem_turnos.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=cores,
        textprops={'color': "black", 'fontsize': 11, 'weight': 'bold'}
    )

    ax.set_title('Número de defeitos por turno')
    ax.set_facecolor((0.29, 0.0, 0.51, 0.25))  # fundo com transparência
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=master)
    return canvas
