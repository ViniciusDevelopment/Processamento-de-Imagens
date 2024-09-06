import requests
from PIL import Image
import numpy as np
import io
import matplotlib.pyplot as plt

url_imagem = "https://www.wikiparques.org/images/thumb/8/8c/2017935485904.jpg/800px-2017935485904.jpg"

# Fazendo o download da imagem
resposta = requests.get(url_imagem)

# Verificando se o download foi bem-sucedido
if resposta.status_code == 200:
    # Usando BytesIO para carregar a imagem diretamente em memória
    imagem_original = Image.open(io.BytesIO(resposta.content))

    # Pegando as proporções da imagem original
    largura_original, altura_original = imagem_original.size

    # Exibindo a imagem original no tamanho original
    plt.figure(figsize=(largura_original/100, altura_original/100))  # Define o tamanho proporcional à imagem original
    plt.imshow(imagem_original)
    plt.title("Imagem Original " + str(largura_original)+" X "+str(altura_original))
    plt.axis('off')  # Desliga os eixos para melhor visualização
    plt.show()

    # Convertendo a imagem para tons de cinza
    imagem_cinza = imagem_original.convert('L')

    # Pegando as proporções da imagem em cinza
    largura, altura = imagem_cinza.size

    # Transformando a imagem em uma tabela com a função .asarray
    img_tabela = np.asarray(imagem_cinza)

    # Transformação para array numerico: Criando uma tabela com o dobro do tamanho da imagem original
    expansao = np.zeros((altura*2, largura*2), dtype=np.uint8)

    # Copia os pixels da foto original para a matriz estendida
    for l in range(0, altura-1):
        for c in range(0, largura-1):
            expansao[l*2, c*2] = img_tabela[l, c]

    # Aplicando interpolação bilinear nos pixels da imagem expandida
    #Preenche os valores vazios em cada pixel
    # para cada pixel (i, j), aplicada a regra de interpolação bilinear nos elementos
    # (i, j+1), (i+1, j), (i+1, j+1), (i+1, j+2), (i+2, j+1)
    for l in range(0, altura*2-1, 2):
        for c in range(0, largura*2-1, 2):
            x = 0
            x += expansao[l, c]
            x += expansao[l, c+1]
            expansao[l, c+1] = (x / 2)  # a: Interpolação horizontal entre pixels na mesma linha.

            x = 0
            x += expansao[l, c]
            x += expansao[l+1, c]
            expansao[l+1, c] = (x / 2)  # b: Interpolação vertical entre pixels na mesma coluna.

            x = 0
            x += expansao[l, c]
            x += expansao[l, c+1]
            x += expansao[l+1, c]
            x += expansao[l+1, c+1]
            expansao[l+1, c+1] = (x / 4)  # c: Interpolação diagonal entre quatro pixels.

            if c+2 <= largura*2-1:
                x = 0
                x += expansao[l, c+1]
                x += expansao[l+1, c+1]
                expansao[l+1, c+2] = (x / 2)  # d: Interpolação para colunas e linhas subsequentes, expandindo a matriz.

            if l+2 <= altura*2-1:
                x = 0
                x += expansao[l+1, c]
                x += expansao[l+1, c+1]
                expansao[l+2, c+1] = (x / 2)  # e: Interpolação para colunas e linhas subsequentes, expandindo a matriz.

    # Transformando a tabela expansao em uma imagem
    nova_img = Image.fromarray(expansao)
    largura_ampliada, altura_ampliada = nova_img.size


    # Exibindo a nova imagem expandida no tamanho correto
    plt.figure(figsize=((largura_ampliada)/100, (altura_ampliada)/100))  # Define o tamanho proporcional à imagem ampliada
    plt.imshow(nova_img, cmap='gray')
    plt.title("Imagem Ampliada "+ str(largura_ampliada)+" X "+str(altura_ampliada))
    plt.axis('off')
    plt.show()
else:
    print("Erro ao baixar a imagem.")
