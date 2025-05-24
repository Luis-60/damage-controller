# import modules
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import csv

# configure workspace
root = tk.Tk()
root.title("Damage Controller")
root.geometry("600x400+50+50")

# function open_csv_file
def open_csv_file():
    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv *.CSV")])
    if file_path:
        display_csv_data(file_path)

def display_csv_data(file_path):
    try:
        with open(file_path, 'r', encoding='latin1', newline='') as file:
            csv_reader = csv.reader(file, delimiter=';')  # use delimiter instead of sep
            header = next(csv_reader)
            tree.delete(*tree.get_children())  # corrigido aqui

            tree["columns"] = header
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            for row in csv_reader:
                tree.insert("", "end", values=row)
            
            status_label.config(text=f"CSV file loaded: {file_path}")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

open_button = tk.Button(root, text="Open CSV file", command=open_csv_file)
open_button.pack(padx=20, pady=10)

tree = ttk.Treeview(root, show="headings")
tree.pack(padx=20, pady=20, fill="both", expand=True)

status_label = tk.Label(root, text="", padx=20, pady=10)
status_label.pack()

# infinite loop
root.mainloop()

#data 
#id veiculo
#turno
#região
#peça
#defeito
#responsavel
#comentario