import pandas as pd
from tkinter import Tk, filedialog

# Esconde a janela principal do Tkinter
Tk().withdraw()

# Abre janela para escolher o arquivo
arquivo = filedialog.askopenfilename(
    title="Selecione o arquivo Excel",
    filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
)

print("Arquivo escolhido:", arquivo)

# Lê todas as abas
planilhas = pd.read_excel(arquivo, sheet_name=None)

# Mostra as abas disponíveis
print("\nAbas encontradas:")
for nome in planilhas.keys():
    print("-", nome)
