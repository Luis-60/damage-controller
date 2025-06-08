import tkinter as tk
from tkinter import ttk, messagebox
from main import processar_dados
import calendar
import pandas as pd

def filtrar_dados(self):
    if self.df is None or self.df.empty:
        messagebox.showwarning("Aviso", "Carregue um arquivo CSV primeiro.")
        return

    filtro_janela = tk.Toplevel(self.master)
    filtro_janela.title("Filtrar Dados")
    filtro_janela.geometry("400x500")
    filtro_janela.configure(bg="#2A2F4F")

    # Scroll para caso haja muitas colunas
    canvas = tk.Canvas(filtro_janela, bg="#2A2F4F", highlightthickness=0)
    frame_filtros = tk.Frame(canvas, bg="#2A2F4F")
    scrollbar = ttk.Scrollbar(filtro_janela, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame_filtros, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame_filtros.bind("<Configure>", on_configure)

    # Dicionário para armazenar as variáveis de filtro
    filtros_vars = {}

    # Filtro de mês (pela coluna DATA)
    tk.Label(frame_filtros, text="Mês:", bg="#2A2F4F", fg="white", anchor="w").pack(pady=5, padx=10, fill="x")
    meses = [""] + [calendar.month_name[i] for i in range(1, 13)]
    var_mes = tk.StringVar()
    cb_mes = ttk.Combobox(frame_filtros, textvariable=var_mes, values=meses, state="readonly")
    cb_mes.pack(padx=10, fill="x")
    filtros_vars['MES'] = var_mes

    # Cria filtro para as demais colunas (exceto DATA, que é tratada no filtro de mês)
    for coluna in self.df.columns:
        if coluna.upper() == 'DATA':
            continue  # pula a coluna DATA

        valores = sorted(self.df[coluna].dropna().astype(str).unique())
        tk.Label(frame_filtros, text=coluna + ":", bg="#2A2F4F", fg="white", anchor="w").pack(pady=5, padx=10, fill="x")
        var = tk.StringVar()
        cb = ttk.Combobox(frame_filtros, textvariable=var, values=[""] + valores, state="readonly")
        cb.pack(padx=10, fill="x")
        filtros_vars[coluna] = var

    def aplicar_filtros():
        df_filtrado = self.df.copy()

        # Aplica filtro de mês
        mes_selecionado = filtros_vars['MES'].get()
        if mes_selecionado:
            # Converte nome do mês para número (1-12)
            try:
                numero_mes = list(calendar.month_name).index(mes_selecionado)
            except ValueError:
                numero_mes = None

            if numero_mes:
                df_filtrado['DATA'] = pd.to_datetime(df_filtrado['DATA'], errors='coerce')
                df_filtrado = df_filtrado[df_filtrado['DATA'].dt.month == numero_mes]

        # Aplica filtros das outras colunas
        for coluna, var in filtros_vars.items():
            if coluna == 'MES':
                continue  # mês já filtrado
            valor = var.get()
            if valor:
                df_filtrado = df_filtrado[df_filtrado[coluna].astype(str) == valor]

        if df_filtrado.empty:
            messagebox.showinfo("Sem resultados", "Nenhum dado encontrado com os filtros selecionados.")
        else:
            self.df = processar_dados(df_filtrado)
            self.atualizar_interface()

        filtro_janela.destroy()

    # Botão aplicar
    tk.Button(frame_filtros, text="Aplicar Filtros", command=aplicar_filtros,
              bg="#E5BEEC", fg="black").pack(pady=20, padx=10, fill="x")

    def limpar_filtros():
        if self.df_original is not None:
            self.df = self.df_original.copy()
            self.df = processar_dados(self.df)
            self.atualizar_interface()
            filtro_janela.destroy()
        else:
            messagebox.showwarning("Aviso", "Dados originais não disponíveis.")

    tk.Button(frame_filtros, text="Limpar Filtros", command=limpar_filtros,
              bg="#FFB6C1", fg="black").pack(pady=5, padx=10, fill="x")
