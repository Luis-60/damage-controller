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

    fig = Figure(figsize=(3.3, 2.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(x=contagem_turnos.values, labels=contagem_turnos.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Número de defeitos por turno')

    canvas = FigureCanvasTkAgg(fig, master=master)
    return canvas
