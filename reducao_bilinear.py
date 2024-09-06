import requests
from PIL import Image
import numpy as np
import io
import matplotlib.pyplot as plt

# URL da imagem que você quer baixar
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

    # Criando uma tabela com a metade do tamanho da imagem original, usei duas barras para retornar o valor inteiro
    reducao  = np.zeros((altura//2, largura//2), dtype=np.uint8)

    #4 pixels da imagem original formam o bloco 2x2
    for l in range (0 , altura - 1, 2):
      for c in range(0, largura -1, 2):
          soma = 0
          soma += img_tabela[l, c] #Começa no canto superior esquerdo | pixel atual
          soma += img_tabela[l, c+1] # vizinho do lado direito
          soma += img_tabela[l+1, c] # vizinho de baixo
          soma += img_tabela[l+1, c+1] # vizinho da diagonal
          reducao[int(l/2), int(c/2)] = (soma / 4) #calculo da média e armazenamento na nova imagem

    # Transformando a tabela expansao em uma imagem
    nova_img = Image.fromarray(reducao)
    largura_ampliada, altura_ampliada = nova_img.size


    # Exibindo a nova imagem expandida no tamanho correto
    plt.figure(figsize=((largura_ampliada)/100, (altura_ampliada)/100))  # Define o tamanho proporcional à imagem ampliada
    plt.imshow(nova_img, cmap='gray')
    plt.title("Imagem Ampliada "+ str(largura_ampliada)+" X "+str(altura_ampliada))
    plt.axis('off')
    plt.show()
else:
    print("Erro ao baixar a imagem.")
