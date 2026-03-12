from cryptography.fernet import Fernet
import os

def retornar_llave():
    return open("llave.llave", 'rb').read()

def desencriptar(items, llave):
    i = Fernet(llave)
    for item in items:
        with open(item, 'rb') as file:
            file_data = file.read()
        data = i.decrypt(file_data)

        with open(item, 'wb') as file:
            file.write(data)

if __name__ == '__main__':
    path = "C:\\Users\\felip\\Desktop\\Curso Angular"
    os.remove(path+"\\"+"readme.txt")
    items = os.listdir(path)
    archivos = [path+"\\"+x for x in items]

llave = retornar_llave()
desencriptar(archivos, llave)