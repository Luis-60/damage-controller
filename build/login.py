import tkinter as tk
from tkinter import messagebox
import pandas as pd


# Função para carregar usuários de um arquivo Excel
def carregar_usuarios():
    """
    Carrega os usuários e senhas de um arquivo Excel.
    Retorna um dicionário com os usuários e senhas.
    """
    try:
        df = pd.read_excel("C:/Users/Kalevi/Downloads/damage-controller-main/damage-controller-main/backend/usuarios.xlsx") # Substitua pelo caminho do seu arquivo Excel
        usuarios = dict(zip(df['Login'], df['Senha']))
        return usuarios
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar os usuários:\n{str(e)}")
        return {}

# Carrega os usuários do Excel
USUARIOS = carregar_usuarios()


def verificar_login(usuario, senha):
    """
    Verifica se o usuário e senha estão corretos.
    """
    if usuario in USUARIOS and USUARIOS[usuario] == senha:
        return True
    return False

def tela_login():
    """
    Cria a interface de login.
    """
    def tentar_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        
        if verificar_login(usuario, senha):
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            root.destroy()  # Fecha a tela de login
           
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
    
    root = tk.Tk()
    root.title("Login")
    
    tk.Label(root, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(root, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = tk.Entry(root, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)
    
    btn_login = tk.Button(root, text="Login", command=tentar_login)
    btn_login.grid(row=2, column=0, columnspan=2, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    tela_login()