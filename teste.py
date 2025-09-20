import os
from PIL import Image

# Substitua pelo nome do arquivo que está no banco
nome_imagem = "MetaltexAdpatdorFuro.png"  

# Caminho relativo à raiz do projeto
caminho_imagem = os.path.join("assets", "images", nome_imagem)

print("Caminho completo:", caminho_imagem)
print("Arquivo existe?", os.path.exists(caminho_imagem))

if os.path.exists(caminho_imagem):
    try:
        img = Image.open(caminho_imagem)
        img.show()  # abre a imagem no visualizador padrão
        print("Imagem carregada com sucesso!")
    except Exception as e:
        print("Erro ao abrir a imagem:", e)
else:
    print("O arquivo não foi encontrado no caminho indicado.")

if __name__ == "__main__":
    app = App()
    app.run()