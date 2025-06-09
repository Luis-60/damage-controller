import tkinter as tk
from tkinter import messagebox
import pandas as pd

def carregar_usuarios():
    try:
        df = pd.read_excel("C:/Users/Kalevi/Downloads/damage-controller-main/damage-controller-main/backend/usuarios.xlsx")
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