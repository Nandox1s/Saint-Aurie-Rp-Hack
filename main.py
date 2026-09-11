import keyboard
from time import sleep
import logic
                
# Programa Principal
while True:
    #desbloquei com ' e em seguida espera o comando do nível do hack
    keyboard.wait("'")
    print("Desbloqueado...")

    tecla = keyboard.read_key()

    if tecla in ["z", "x", "c", "'"]:
        while tecla == "'":
            sleep(0.25)
            tecla = keyboard.read_key()

        tecla = keyboard.read_key()
        logic.escolhas(tecla)
    