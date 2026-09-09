import pyautogui
import cv2
import mss
import numpy as np
from time import sleep

# Posição do alvo e do quadro
def alvo():

    print("def alvo")

    mouse = pyautogui.position()

    mouse_loc = {
        "left": mouse[0],
        "top": mouse[1],
        "width": 32,
        "height": 20
    }

    return mouse_loc


# Programa que procura o template
def procurar(quadro):

    print("def procurar")

    ok = 0

    with mss.MSS() as sct:

        # Criação do array da imagem
        imagem_alvo = np.array(sct.grab(alvo()))
        imagem_alvo = cv2.cvtColor(imagem_alvo, cv2.COLOR_BGRA2GRAY)

        # Salva o alvo
        cv2.imwrite("prints/alvo.png", imagem_alvo)

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
            if confianca >= 0.55:

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
                cv2.imwrite("prints/encontrado.png", encontrado)

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

                    sleep(0.005)

                return print("feito")