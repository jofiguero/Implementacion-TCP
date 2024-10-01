import socket
from t2 import  Mensaje_TCP, conectar, enviar

def formar_input():
    mensaje = input("Introduzca el mensaje" )
    ack = input("Introduzca el ack ")
    syn = input("Introduzca el syn ")
    fin = input("Introduzca el fin ")
    return Mensaje_TCP(mensaje, int(ack), int(syn), int(fin))

def generar_mensaje_enorme(min_size):
    mensaje = ""
    while len(mensaje) < min_size:
        mensaje += "aaaaa"
        mensaje += "bbbbb"
        mensaje += "ccccc"
        mensaje += "ddddd"
        mensaje += "eeeee"
        mensaje += "fffff"
    return mensaje




sock = conectar('127.0.0.1',12345)


while True:
    
    desicion = input("¿Quieres enviar un mensaje propio (1) o un mensaje muy largo autogenerado (2)? ")

    if desicion == "1":
        mensaje = input("Ingresa tu mensaje: ")
        break

    elif desicion == "2":
        mensaje = generar_mensaje_enorme(int(input("Ingresa el largo que quieres que tenga el mensaje: ")))
        break

    else: 
        print("Input no valido")

if len(mensaje) > 1000:
    print("El mensaje ingresado es bastante largo, esto podria tardar mas de un minuto...")

enviar(sock, mensaje)

print("En tres segundos el mensaje enviado debería aparecer en la otra consola")