import pyautogui
from time import sleep
sleep(1)

for x in range(0,3):
    sleep(2)
    posicao_inicial = pyautogui.position()
    print("próximo")
    sleep(2)
    posicao_final = pyautogui.position()

    w = posicao_final[0]-posicao_inicial[0]
    h = posicao_final[1]-posicao_inicial[1]
    l = posicao_inicial[0]
    t = posicao_inicial[1]

    print(f"(\"left\":{l},\"top\":{t},\"width\":{w},\"height\":{h})")

