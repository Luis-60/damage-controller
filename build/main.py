import pandas as pd
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import locale
import re
import tkinter as tk
from login import tela_login


def iniciar_aplicacao():
    root = tk.Tk()
    root.withdraw()  # Oculta até que login seja bem-sucedido

    if tela_login(root):  # Aguarda e retorna True/False
        from gui import main as abrir_gui
        root.deiconify()  # Exibe a janela principal
        abrir_gui(root)  # passa a janela já existente
        root.mainloop()
    else:
        root.destroy()  # Encerra tudo

if __name__ == "__main__":
    iniciar_aplicacao()

# Configuração de locale para datas em português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except:
        print("Aviso: Locale não configurado. Datas podem não aparecer em português.")

def carregar_csv():
    """
    Abre diálogo para selecionar e carregar arquivo CSV
    Retorna um DataFrame pandas ou None em caso de erro
    """
    try:
        file_path = filedialog.askopenfilename(
            title="Selecionar Arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if not file_path:
            return None
            
        # Tenta detectar automaticamente o separador e encoding
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='latin1', on_bad_lines='warn')
        
        # Verifica colunas essenciais
        colunas_necessarias = {'DEFEITOS', 'RESPONSÁVEL'}
        if not colunas_necessarias.issubset(df.columns):
            cols_faltantes = colunas_necessarias - set(df.columns)
            messagebox.showwarning(
                "Colunas faltando",
                f"O arquivo não contém colunas necessárias: {', '.join(cols_faltantes)}"
            )
            return None
            
        return df
        
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar o arquivo:\n{str(e)}")
        return None

def processar_dados(df):
    """
    Processa o DataFrame para análise:
    - Preenche valores vazios
    - Filtra linhas sem defeitos
    - Converte colunas de data
    Retorna o DataFrame processado
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Padroniza nomes de colunas (opcional)
    df.columns = df.columns.str.upper()
    
    # Preenche valores vazios
    colunas_para_preencher = ['RESPONSÁVEL', 'DEFEITOS', 'REGIÃO', 'PEÇA']
    for col in colunas_para_preencher:
        if col in df.columns:
            df[col] = df[col].fillna('')
    
    # Filtra linhas sem defeitos
    if 'DEFEITOS' in df.columns:
        df['DEFEITOS'] = df['DEFEITOS'].str.upper().str.strip()

        padrao_sem_defeito = r'\b(?:SEM\s+DEFEITO|VE[IÍ]CULO\s+SEM\s+DEFEITO|O\s+SEM\s+DEFEITO|NENHUM|NAO\s+TEM\s+DEFEITO|NÃO\s+TEM\s+DEFEITO|OK)\b'
        df = df[~df['DEFEITOS'].str.contains(padrao_sem_defeito, na=False, regex=True)]

    return df

def gerar_grafico_responsavel(df, master):
    """
    Gera o gráfico de defeitos por responsável
    Retorna um FigureCanvasTkAgg pronto para exibição
    """
    fig = Figure(figsize=(3.0, 2.5), facecolor="#917FB3")
    ax = fig.add_subplot()
    ax.set_facecolor("#917FB3")
    
    if df.empty or 'RESPONSÁVEL' not in df.columns:
        ax.text(0.5, 0.5, 'Sem dados disponíveis', 
                ha='center', va='center', color='white')
        return FigureCanvasTkAgg(fig, master=master)
    
    contagem = df['RESPONSÁVEL'].value_counts().head(5)
    
    bars = ax.bar(contagem.index, contagem.values, color='#E5BEEC', edgecolor='black')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f'{int(height)}',
                ha='center', va='bottom', fontsize=7, color='white')
    
    ax.set_title('Defeitos por Responsável', fontsize=8, color='white', pad=10)
    ax.set_xlabel('')
    ax.set_ylabel('Qtd. Defeitos', fontsize=7, color='white')
    ax.tick_params(axis='x', rotation=45, labelsize=7, colors='white')
    ax.tick_params(axis='y', labelsize=7, colors='white')
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='white')
    
    return FigureCanvasTkAgg(fig, master=master)

def exportar_relatorio(df, file_path):
    """
    Exporta um relatório consolidado para Excel
    Retorna True se bem sucedido, False caso contrário
    """
    try:
        with pd.ExcelWriter(file_path) as writer:
            # Relatório por responsável
            if 'RESPONSÁVEL' in df.columns:
                df_resp = df['RESPONSÁVEL'].value_counts().reset_index()
                df_resp.columns = ['Responsável', 'Qtd. Defeitos']
                df_resp.to_excel(writer, sheet_name='Por Responsável', index=False)
            
            # Relatório por categoria
            if 'DEFEITOS' in df.columns:
                df_defeitos = df['DEFEITOS'].value_counts().reset_index()
                df_defeitos.columns = ['Tipo de Defeito', 'Qtd. Ocorrências']
                df_defeitos.to_excel(writer, sheet_name='Por Defeito', index=False)
            
            # Relatório por mês (se disponível)
            if 'MÊS' in df.columns:
                df_mes = df['MÊS'].value_counts().reset_index()
                df_mes.columns = ['Mês', 'Qtd. Defeitos']
                df_mes.to_excel(writer, sheet_name='Por Mês', index=False)
        
        return True
    except Exception as e:
        print(f"Erro ao exportar relatório: {e}")
        return False