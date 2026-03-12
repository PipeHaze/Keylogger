
from pynput.mouse import Listener

def listener_mouse(x, y):
    print(f'La posicion del mouse es {x} : {y}')

with Listener(on_move = listener_mouse) as l:
    l.join()

"""
from pynput.keyboard import Listener

def listener_teclado(key):
    letra = str(key)
    letra = letra.replace(".", "")

    if letra == 'Key.space':
        letra = ' '
    with open("log.txt", 'a') as f:
        f.write(letra)

with Listener(on_press = listener_teclado) as l:
    l.join()
"""

