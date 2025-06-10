import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os 
import customtkinter  # Certifique-se de que customtkinter está instalado

janela = customtkinter.CTk()
janela.geometry("900x600")

def carregar_usuarios():
    try:
        # Pega o caminho da pasta onde está o script atual
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        # Sobe uma pasta para chegar na pasta que contém 'backend'
        pasta_projeto = os.path.dirname(pasta_atual)
        # Monta o caminho para o arquivo dentro da pasta 'backend'
        caminho_arquivo = os.path.join(pasta_projeto, 'backend', 'usuarios.xlsx')

        df = pd.read_excel(caminho_arquivo)
        return dict(zip(df['Login'], df['Senha']))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar usuários:\n{str(e)}")
        return {}

USUARIOS = carregar_usuarios()

def verificar_login(usuario, senha):
    return usuario in USUARIOS and USUARIOS[usuario] == senha

def tela_login(root):
    sucesso = {"ok": False}

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.grab_set()

    def tentar_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if verificar_login(usuario, senha):
            sucesso["ok"] = True
            login_window.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    # Layout
    tk.Label(login_window, text="Usuário").grid(row=0, column=0)
    entry_usuario = tk.Entry(login_window)
    entry_usuario.grid(row=0, column=1)

    tk.Label(login_window, text="Senha").grid(row=1, column=0)
    entry_senha = tk.Entry(login_window, show="*")
    entry_senha.grid(row=1, column=1)

    tk.Button(login_window, text="Login", command=tentar_login).grid(columnspan=2, pady=10)

    login_window.wait_window()  # Aguarda login ser fechado
    return sucesso["ok"]