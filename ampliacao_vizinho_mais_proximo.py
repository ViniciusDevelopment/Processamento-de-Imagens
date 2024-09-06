import requests
from PIL import Image
import numpy as np
import io
import matplotlib.pyplot as plt
import pandas as pd

# URL da imagem que você quer baixar
url_imagem = "https://www.wikiparques.org/images/thumb/8/8c/2017935485904.jpg/800px-2017935485904.jpg"

# Fazendo o download da imagem
resposta = requests.get(url_imagem)

# Verificando se o download foi bem-sucedido
if resposta.status_code == 200:
    imagem_original = Image.open(io.BytesIO(resposta.content))

    # Pegando as proporções da imagem original
    largura_original, altura_original = imagem_original.size


    # Convertendo a imagem para tons de cinza
    imagem_cinza = imagem_original.convert('L')

    # Transformando a imagem em uma tabela com a função .asarray
    img_tabela = np.asarray(imagem_cinza)

    # Exibindo a matriz de pixels da imagem original
    df_original = pd.DataFrame(img_tabela)
    print("Matriz de Pixels da Imagem Original:")
    print(df_original)

    # Criando uma tabela com o dobro do tamanho da imagem original para ampliação (vizinho mais próximo)
    altura, largura = img_tabela.shape
    expansao = np.zeros((altura*2, largura*2), dtype=np.uint8)

    # Aplicando o método do vizinho mais próximo. O ponto principal é trabalhar com as linhas pares
    for l in range(altura):
        for c in range(largura):
            expansao[l*2, c*2] = img_tabela[l, c]  # Pixel original
            expansao[l*2, c*2+1] = img_tabela[l, c]  # Copia para a direita
            expansao[l*2+1, c*2] = img_tabela[l, c]  # Copia para baixo
            expansao[l*2+1, c*2+1] = img_tabela[l, c]  # Copia para diagonal inferior direita

    # Exibindo a matriz de pixels da imagem ampliada
    df_ampliada = pd.DataFrame(expansao)
    print("\nMatriz de Pixels da Imagem Ampliada (Vizinho Mais Próximo):")
    print(df_ampliada)

    # Exibindo a imagem original no tamanho original
    plt.figure(figsize=(largura_original/100, altura_original/100))  # Define o tamanho proporcional à imagem original
    plt.imshow(imagem_original)
    plt.title("Imagem Original " + str(largura_original)+" X "+str(altura_original))
    plt.axis('off')  # Desliga os eixos para melhor visualização
    plt.show()

    # Exibindo a imagem ampliada
    plt.figure(figsize=(largura*2/100, altura*2/100))
    plt.imshow(expansao, cmap='gray')
    plt.title("Imagem Ampliada (Vizinho Mais Próximo)")
    plt.axis('off')
    plt.show()

else:
    print("Erro ao baixar a imagem.")
