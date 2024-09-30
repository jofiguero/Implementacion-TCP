from redest2.t2 import Mensaje_TCP
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

print(generar_mensaje_enorme(50000))