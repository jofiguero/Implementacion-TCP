import socket
from TCP import  Mensaje_TCP, conectar, enviar

def formar_input():
    mensaje = input("Introduzca el mensaje" )
    ack = input("Introduzca el ack ")
    syn = input("Introduzca el syn ")
    fin = input("Introduzca el fin ")
    return Mensaje_TCP(mensaje, int(ack), int(syn), int(fin))



sock = conectar('127.0.0.1',12345)

enviar(sock,"Finalmente pudimos conectarnos!!")
