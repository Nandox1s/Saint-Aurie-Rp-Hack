import pyautogui
import keyboard
import cv2
import mss
import mss.tools
import numpy as np
from time import sleep


# Variáveis
quadro = {
    "left": 1045,
    "top": 351,
    "width": 472,
    "height": 455
}  # dividir quadro em 3


# Posição do alvo e do quadro
def alvo():

    print("def alvo")

    mouse = pyautogui.position()

    mouse_loc = {
        "left": mouse[0],
        "top": mouse[1],
        "width": 25,
        "height": 20
    }

    return mouse_loc


# Programa que procura o template
def procurar():

    print("def procurar")

    ok = 0

    with mss.MSS() as sct:

        # Criação do array da imagem
        imagem_alvo = np.array(sct.grab(alvo()))
        imagem_alvo = cv2.cvtColor(imagem_alvo, cv2.COLOR_BGRA2GRAY)

        # Salva o alvo
        cv2.imwrite("alvo.png", imagem_alvo)

        while ok != 1:

            # Atualiza a imagem do quadro
            imagem_tela = np.array(sct.grab(quadro))
            imagem_tela = cv2.cvtColor(imagem_tela, cv2.COLOR_BGRA2GRAY)

            # Procura o alvo
            resultado = cv2.matchTemplate(
                imagem_tela,
                imagem_alvo,
                cv2.TM_CCOEFF_NORMED
            )

            _, confianca, _, posicao = cv2.minMaxLoc(resultado)

            # 1. Achou a imagem
            print("procurando...")
            if confianca >= 0.6:

                print("Alvo encontrado! ", posicao, "Confiança: ",confianca)

                # Recorta exatamente a região encontrada
                x, y = posicao

                altura_alvo = imagem_alvo.shape[0]
                largura_alvo = imagem_alvo.shape[1]

                encontrado = imagem_tela[
                    y:y + altura_alvo,
                    x:x + largura_alvo
                ]

                # Salva o que foi encontrado
                cv2.imwrite("encontrado.png", encontrado)

                # 2. Espera a imagem mudar
                while True:

                    imagem_atual = np.array(sct.grab(quadro))
                    imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_BGRA2GRAY)

                    # Recorta exatamente a mesma área encontrada anteriormente 
                    regiao_atual = imagem_atual[
                        y:y + altura_alvo,
                        x:x + largura_alvo 
                    ]

                    diferenca = cv2.absdiff(encontrado, regiao_atual)

                    if np.any(diferenca > 10):
                        print("mudou",posicao)
                        pyautogui.click()
                        ok = 1
                        print("ok")
                        break

                    sleep(0.05)

                return print("feito")
                
# Programa Principal

while True:
    keyboard.wait("z")
    procurar()
    

