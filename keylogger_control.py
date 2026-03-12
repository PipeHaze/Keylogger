from pynput.keyboard import Controller
from pynput.mouse import Controller
import sys

def ControlTeclado():
    teclado = Controller()
    teclado.type('')

def ControlMouse():
    mouse = Controller()
    mouse.position = (1200, 800)

def main():
    ControlMouse()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()