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

    # Ajustando as dimensões para lidar com dimensões ímpares
    altura, largura = img_tabela.shape
    nova_altura = altura // 2
    nova_largura = largura // 2

    # Criando uma tabela com metade do tamanho da imagem original para redução (vizinho mais próximo)
    reducao = np.zeros((nova_altura, nova_largura), dtype=np.uint8)

    # Aplicando o método do vizinho mais próximo para redução
    for l in range(0, nova_altura):
        for c in range(0, nova_largura):
            reducao[l, c] = img_tabela[l * 2, c * 2]  # Mantém apenas um pixel a cada 2x2

    # Exibindo a matriz de pixels da imagem reduzida
    df_reduzida = pd.DataFrame(reducao)
    print("\nMatriz de Pixels da Imagem Reduzida (Vizinho Mais Próximo):")
    print(df_reduzida)

    # Exibindo a imagem original no tamanho original
    plt.figure(figsize=(largura_original / 100, altura_original / 100))  # Define o tamanho proporcional à imagem original
    plt.imshow(imagem_original)
    plt.title("Imagem Original " + str(largura_original) + " X " + str(altura_original))
    plt.axis('off')  # Desliga os eixos para melhor visualização
    plt.show()

    # Exibindo a imagem reduzida
    plt.figure(figsize=(nova_largura / 100, nova_altura / 100))
    plt.imshow(reducao, cmap='gray')
    plt.title("Imagem Reduzida (Vizinho Mais Próximo)")
    plt.axis('off')
    plt.show()

else:
    print("Erro ao baixar a imagem.")
