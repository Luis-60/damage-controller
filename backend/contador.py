import pandas as pd


arquivo_csv = r'C:\Users\kalve\Documents\damage-controller\backend\Banco_de_Dados 2.CSV'



df = pd.read_csv(arquivo_csv, encoding='latin1', sep=';', on_bad_lines='skip')


contador_def=df['DEFEITOS'].value_counts()

print(df['DATA'].unique())
