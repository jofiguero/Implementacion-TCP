import socket
import time
import threading

class Mensaje_TCP:
    def __init__(self, mensaje, ACK, SYN, FIN):
        self.mensaje = mensaje
        self.ACK = ACK
        self.SYN = SYN
        self.FIN = FIN
    
    def __str__(self):
        return f"{self.mensaje}|{self.ACK}|{self.SYN}|{self.FIN}"

def parsear_tcp(string):
    string_spliteado = string.split("|")
    return Mensaje_TCP(string_spliteado[0],int(string_spliteado[1]),int(string_spliteado[2]),int(string_spliteado[3]))

def dividir_mensaje(mensaje,maximo):
    return [mensaje[i:i + maximo] for i in range(0, len(mensaje), maximo)]

# Funcion para establecer conexion
def conectar(direccion, puerto):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Fijamos un puerto y una direccion especificas para el socket
    sock.connect((direccion,puerto))

    # Enviamos un mensaje con syn activado
    print("Solicitando conexion")
    sock.send(str(Mensaje_TCP("",0,1,0)).encode())

    # Esperamos recibir un mensaje con syn y ack activados
    data = sock.recv(1024)
    mensaje_decodificado = parsear_tcp(data.decode())

    if mensaje_decodificado.SYN == 1 and mensaje_decodificado.ACK == 1:
        print("Recibimos respuesta, confirmamos de vuelta")
        sock.send(str(Mensaje_TCP("",1,0,0)).encode())
        print("Conexión establecida")
        return sock
    else:
        raise ConnectionError("No se pudo establecer la conexión.")


# Funcion para enviar datos
def enviar(sock, mensaje):
    #Enviamos el mensaje
    mensaje = Mensaje_TCP(mensaje, 0,0,0)
    sock.send(str(mensaje).encode())

    #Esperamos una respuesta
    respuesta = parsear_tcp(sock.recv(1024).decode())

    #Verificamos si es el ACK
    if respuesta.ACK == 1:
        print("Mensaje enviado correctamente.")
    else: 
        print("Pucha no recibimos bien la custion")


# Funcion para recibir datos
def recibir(sock):
    data = sock.recv(1024)
    
    respuesta = Mensaje_TCP("",1,0,0)
    sock.send(str(respuesta).encode())

    return parsear_tcp(data.decode()).mensaje


# Funcion para cerrar la conexion
def terminar(sock):
    # Enviamos un mensaje con fin activado
    print("Solicitando conexion")
    sock.send(str(Mensaje_TCP("",0,0,1)).encode())

    # Esperamos recibir un mensaje con fin y ack activados
    data = sock.recv(1024)
    mensaje_decodificado = parsear_tcp(data.decode())

    if mensaje_decodificado.FIN == 1 and mensaje_decodificado.ACK == 1:
        print("Recibimos respuesta, confirmamos de vuelta")
        sock.send(str(Mensaje_TCP("",1,0,0)).encode())
        print("Conexión finalizada")
        sock.close()
