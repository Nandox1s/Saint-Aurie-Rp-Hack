import pyautogui
import cv2
import mss
import numpy as np
from time import sleep
import config
from keyboard import wait

#Escolha de níveis
def escolhas(tecla):
    if tecla == "z":
        for i in range(0,2):
            procurar(config.area1,0.55)
            wait("z")
        procurar(config.area1,0.55)
        print("Nível 1 finalizado")

    if tecla == "x":
        print("Nível 2")

    if tecla == "c":
        procurar(config.area3,0.7)
        print("Nível 3 finalizado")

# Posição do alvo e do area
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
def procurar(area,var_conf):

    ok = 0

    with mss.MSS() as sct:

        # Criação do array da imagem
        imagem_alvo = np.array(sct.grab(alvo()))
        imagem_alvo = cv2.cvtColor(imagem_alvo, cv2.COLOR_BGRA2GRAY)

        # Salva o alvo
        cv2.imwrite("prints/alvo.png", imagem_alvo)

        while ok != 1:

            # Atualiza a imagem do area
            imagem_tela = np.array(sct.grab(area))
            imagem_tela = cv2.cvtColor(imagem_tela, cv2.COLOR_BGRA2GRAY)

            # Procura o alvo
            resultado = cv2.matchTemplate(
                imagem_tela,
                imagem_alvo,
                cv2.TM_CCOEFF_NORMED
            )

            _, confianca, _, posicao = cv2.minMaxLoc(resultado)

            # 1. Achou a imagem
            if confianca >= var_conf:

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
                if area["left"] == 840:
                    x_mod = posicao[0] + 840
                    y_mod = posicao[1] + 360
                    pyautogui.click(x_mod,y_mod)
                    break

                # 2. Espera a imagem mudar
                while True:

                    imagem_atual = np.array(sct.grab(area))
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
                        break

                    sleep(0.0025)

