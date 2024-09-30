import socket
from redest2.t2 import  parsear_tcp, Mensaje_TCP, recibir

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

# Creamos un socket y lo dejamos escuchando en cualquier direccion
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', 12345))

print("QUEDAMOS ESPERANDO ALGUN MENSAJE")
data, addr = udp_socket.recvfrom(1024)
recibido = parsear_tcp(data.decode())

udp_socket.sendto(str(Mensaje_TCP("",1,1,0,0,1)).encode(), addr)
data, addr = udp_socket.recvfrom(1024)

recibido = parsear_tcp(data.decode())
print("Conexion establecida")

#Conectamos manualmente udp_socket:
udp_socket.connect(addr)

mensaje = recibir(udp_socket)

if mensaje == generar_mensaje_enorme(1000):
    print(mensaje)
    print("El mensaje fue recibido con exito")
else:
    print("El mensaje no llegó correctamente")




