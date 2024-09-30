import socket
from redest2.t2 import  Mensaje_TCP, conectar, enviar

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
mensaje_corto = "Hola como estás juan carlos, yo por mi parte estoy tranquilo, me comentas!"
mensaje_largo = "Te acuerdas que tenia que entregar una tarea de redes hace un tiempo? bueno, paso que la tenia casi lista el dia de la entrega, pero movieron el plazo hacia el dia siguiente y pensé que sería hasta el final del día. Lamentablemente al llegar a la universidad me enteré por mi amigo sebastian que el plazo habia sido movido unicamente hasta las 9 de la mañana del dia, y ya eran las 10. hable con el profesor para ver si se podia llegar a algun tipo de acuerdo sin embargo fue inutil, tuve un 1 en esa tarea."
enviar(sock, generar_mensaje_enorme(1000))