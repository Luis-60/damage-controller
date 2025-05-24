import csv
import os

ARQUIVO_CSV = 'dados.csv'
CAMPOSDOBANCO = ['Data', 'Id do veículo', 'Região', 'Peça afetada', 'Defeito', 'Responsável']


REGIOES = ['']

def criar_csv_se_nao_existir():
    if not os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CAMPOSDOBANCO)
            writer.writeheader()




"""
def create_csv_if_not_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def add_row(row):
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(row)

def update_row(row_id, updated_data):
    rows = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == str(row_id):
                row.update(updated_data)
            rows.append(row)
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

def read_all():
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Exemplo de uso:
if __name__ == '__main__':
    create_csv_if_not_exists()
    add_row({'id': '1', 'name': 'Item1', 'value': '100'})
    add_row({'id': '2', 'name': 'Item2', 'value': '200'})
    update_row('1', {'value': '150'})
    print(read_all())
"""

criar_csv_se_nao_existir()