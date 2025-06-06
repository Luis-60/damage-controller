from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from main import carregar_csv, processar_dados, gerar_grafico_responsavel, gerar_grafico_categorias, gerar_grafico_mensal, exportar_relatorio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.responsavel import gerar_grafico_responsavel


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
        self.setup_treeview()
        
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
        self.create_section(54.0, 114.0, 348.0, 276.0, "Regiões e peças com maior número de defeitos")
        self.create_section(54.0, 286.0, 307.0, 515.0, "Número de Defeitos por Categoria")
        self.create_section(321.0, 286.0, 631.0, 515.0, "Número de Defeitos por Mês")
        self.create_section(644.0, 286.0, 945.0, 515.0, "Número de Defeitos por Responsável")
        self.create_section(361.0, 114.0, 652.0, 276.0, "Número de Defeitos por Categoria")
        self.create_section(666.0, 114.0, 945.0, 276.0, "Número de Defeitos por Dia")
        
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
        self.btn_load.place(x=376.0, y=26.0, width=117.0, height=25.0)
        
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
        self.btn_export.place(x=507.0, y=26.0, width=117.0, height=25.0)
        
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
        
    def setup_treeview(self):
        # Treeview para visualização rápida dos dados
        self.tree_frame = tk.Frame(self.master, bg="#2A2F4F")
        self.tree_frame.place(x=50, y=80, width=900, height=30)
        
        self.tree = ttk.Treeview(self.tree_frame, height=1)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
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
            
        # Atualiza Treeview
        self.atualizar_treeview()
        
        # Atualiza gráficos
        self.atualizar_graficos()
        
    def atualizar_treeview(self):
        """Atualiza a exibição dos dados na Treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if self.df is None or self.df.empty:
            return
            
        self.tree["columns"] = list(self.df.columns)
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
            
        for _, row in self.df.head(10).iterrows():
            self.tree.insert("", "end", values=list(row))
            
    def atualizar_graficos(self):
        self.canvas_resp = gerar_grafico_responsavel(self.df, self.master)
        self.canvas_resp.draw()
        self.canvas_resp.get_tk_widget().place(x=644, y=286)
        
        # Gráfico por categoria
        self.canvas_cat = gerar_grafico_categorias(self.df, self.master)
        self.canvas_cat.draw()
        self.canvas_cat.get_tk_widget().place(x=54, y=286)
        
        # Gráfico por mês (se existir dados de mês)
        if 'MÊS' in self.df.columns:
            self.canvas_mes = gerar_grafico_mensal(self.df, self.master)
            self.canvas_mes.draw()
            self.canvas_mes.get_tk_widget().place(x=321, y=286)
            
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
        """Filtra os dados conforme critérios (implementar lógica específica)"""
        messagebox.showinfo("Info", "Funcionalidade de filtro será implementada aqui")
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = DamageControllerApp(root)
    root.mainloop()
