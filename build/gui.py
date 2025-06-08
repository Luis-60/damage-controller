from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from main import carregar_csv, processar_dados, exportar_relatorio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.responsavel import gerar_grafico_responsavel
from backend.turno import gerar_grafico_turno
from backend.mensal import gerar_grafico_mensal
from backend.categoria import gerar_grafico_categoria
from backend.dia import gerar_grafico_por_dia
from backend.regiao_peca import gerar_grafico_regiao_peca


class DamageControllerApp:
    def __init__(self, master):
        self.master = master
        self.df = None
        self.setup_ui()
        self.setup_style()
        
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Inter', 10), padding=6)
        style.configure('TLabel', font=('Inter', 10), background='#2A2F4F', foreground='white')
        
    def setup_ui(self):
        self.master.title("Damage Controller")
        self.master.geometry("1000x550")
        self.master.configure(bg="#2A2F4F")
        self.master.resizable(False, False)
        
        self.setup_canvas()
        self.setup_buttons()

        
    def setup_canvas(self):
        self.canvas = tk.Canvas(
            self.master,
            bg="#2A2F4F",
            height=550,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Cabeçalho
        self.canvas.create_rectangle(
            0.0, 0.0, 1000.0, 72.0,
            fill="#E5BEEC",
            outline=""
        )
        
        self.canvas.create_text(
            85.0, 20.0,
            anchor="nw",
            text="Damage Controller",
            fill="#000000",
            font=("Inter Bold", 30)
        )
        
        # Áreas dos gráficos
        self.create_section(54.0, 90.0, 348.0, 276.0, "Defeitos por Categoria")
        self.create_section(54.0, 286.0, 307.0, 515.0, "Defeitos por turno")
        self.create_section(321.0, 286.0, 631.0, 515.0, "Regiões e peças")
        self.create_section(644.0, 286.0, 945.0, 515.0, "Defeitos por Responsável")
        self.create_section(361.0, 90.0, 652.0, 276.0, "Defeitos por Mês")
        self.create_section(666.0, 90.0, 945.0, 276.0, "Defeitos por Dia")
        
    def create_section(self, x1, y1, x2, y2, title):
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#917FB3",
            outline=""
        )
        self.canvas.create_text(
            x1+17, y1+18,
            anchor="nw",
            text=title,
            fill="#FFFFFF",
            font=("Inter Bold", 10)
        )
        
    def setup_buttons(self):
        # Botão Carregar CSV
        self.btn_load = tk.Button(
            self.master,
            text="Carregar CSV",
            command=self.carregar_dados,
            bg="#E5BEEC",
            fg="#000000",
            font=("Inter", 10),
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.btn_load.place(x=476.0, y=26.0, width=117.0, height=25.0)
        
        # Botão Exportar Relatório
        self.btn_export = tk.Button(
            self.master,
            text="Exportar Relatório",
            command=self.exportar_dados,
            bg="#E5BEEC",
            fg="#000000",
            font=("Inter", 10),
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.btn_export.place(x=600.0, y=26.0, width=117.0, height=25.0)
        
        # Outros botões (pode adicionar funcionalidades depois)
        self.btn_filter = tk.Button(
            self.master,
            text="Filtrar Dados",
            command=self.filtrar_dados,
            bg="#E5BEEC",
            fg="#000000",
            font=("Inter", 10),
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.btn_filter.place(x=773.0, y=47.0, width=107.0, height=25.0)
        
        self.btn_help = tk.Button(
            self.master,
            text="Ajuda",
            command=self.mostrar_ajuda,
            bg="#E5BEEC",
            fg="#000000",
            font=("Inter", 10),
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.btn_help.place(x=880.0, y=47.0, width=120.0, height=25.0)
        

        
    def carregar_dados(self):
        """Carrega e processa os dados do CSV"""
        df = carregar_csv()
        if df is not None:
            self.df = processar_dados(df)
            self.atualizar_interface()
            
    def atualizar_interface(self):
        """Atualiza todos os elementos da interface com os novos dados"""
        if self.df is None or self.df.empty:
            return
        
        # Atualiza gráficos
        self.atualizar_graficos()
        
            
    def atualizar_graficos(self):
        """Atualiza todos os gráficos na interface"""
        # Remove gráficos antigos
        for attr in ['canvas_resp', 'canvas_cat', 'canvas_mes', 'canvas_cat_fr', 'canvas_dia', 'canvas_reg']:
            if hasattr(self, attr):
                getattr(self, attr).get_tk_widget().destroy()
        
        #responsável
        self.canvas_resp = gerar_grafico_responsavel(self.df, self.master)
        self.canvas_resp.draw()
        self.canvas_resp.get_tk_widget().place(x=644, y=286)
        
        #turno
        self.canvas_cat = gerar_grafico_turno(self.df, self.master)
        self.canvas_cat.draw()
        self.canvas_cat.get_tk_widget().place(x=54, y=286)

        #categoria
        self.canvas_cat_fr = gerar_grafico_categoria(self.df, self.master)
        self.canvas_cat_fr.draw()
        self.canvas_cat_fr.get_tk_widget().place(x=54, y=90)

        #mês
        self.canvas_mes = gerar_grafico_mensal(self.df, self.master)
        self.canvas_mes.draw()
        self.canvas_mes.get_tk_widget().place(x=361.0, y=90)

        #dia
        self.canvas_dia = gerar_grafico_por_dia(self.df, self.master)
        self.canvas_dia.draw()
        self.canvas_dia.get_tk_widget().place(x=666.0, y=90)

        #região e peça
        self.canvas_reg = gerar_grafico_regiao_peca(self.df, self.master)
        self.canvas_reg.draw()
        self.canvas_reg.get_tk_widget().place(x=321.0, y=286)
            
    def exportar_dados(self):
        """Exporta os dados para um arquivo Excel"""
        if self.df is None or self.df.empty:
            messagebox.showwarning("Aviso", "Não há dados para exportar!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Arquivo Excel", "*.xlsx"), ("Todos os arquivos", "*.*")],
            title="Salvar Relatório"
        )
        
        if file_path:
            success = exportar_relatorio(self.df, file_path)
            if success:
                messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível exportar o relatório")
                
    def filtrar_dados(self):
       from TesteFiltro import filtrar_dados
       filtrar_dados(self)
        
    def mostrar_ajuda(self):
        """Mostra informações de ajuda"""
        messagebox.showinfo(
            "Ajuda",
            "Damage Controller v1.0\n\n"
            "1. Use 'Carregar CSV' para importar seus dados\n"
            "2. Visualize os gráficos automaticamente gerados\n"
            "3. Exporte relatórios com 'Exportar Relatório'\n\n"
            "Suporte: contato@damagecontroller.com"
        )
    def carregar_dados(self):
        from main import carregar_csv, processar_dados  # Importa suas funções utilitárias

        self.df = carregar_csv()
        if self.df is not None:
            self.df_original = self.df.copy()  # Armazena cópia original para limpar filtros depois
            self.df = processar_dados(self.df)
            self.atualizar_interface()
        else:
            messagebox.showinfo("Erro", "Nenhum dado foi carregado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DamageControllerApp(root)
    root.mainloop()


