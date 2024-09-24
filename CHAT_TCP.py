import socket
import time
import threading

# Constantes para el Handshake
SYN = "SYN"
SYN_ACK = "SYN-ACK"
ACK = "ACK"

# Tiempo de espera para reenvio de paquetes en segundos
TIMEOUT = 2
MAX_ATTEMPTS = 5

def enviar_mensaje(direccion,puerto,mensaje):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(TIMEOUT)
    udp_socket.sendto(mensaje.encode(), (direccion, puerto))

# Funcion para establecer conexion
def conectar(direccion, puerto):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(TIMEOUT)

    # Enviar SYN (iniciar handshaking)
    print("Enviando SYN...")
    udp_socket.sendto(SYN.encode(), (direccion, puerto))

    # Recibir SYN-ACK
    for attempt in range(MAX_ATTEMPTS):
        try:
            data, addr = udp_socket.recvfrom(1024)
            if data.decode() == SYN_ACK:
                print("Recibido SYN-ACK. Enviando ACK...")
                udp_socket.sendto(ACK.encode(), addr)
                print("Conexión establecida.")
                return udp_socket
        except socket.timeout:
            print(f"Intento {attempt + 1}/{MAX_ATTEMPTS}: No se recibió SYN-ACK. Reintentando...")
            udp_socket.sendto(SYN.encode(), (direccion, puerto))

    raise ConnectionError("No se pudo establecer la conexión.")

# Funcion para enviar datos
def enviar(sock, mensaje):
    attempts = 0
    ack_received = False

    while attempts < MAX_ATTEMPTS and not ack_received:
        sock.sendto(mensaje.encode(), sock.getpeername())
        try:
            ack, addr = sock.recvfrom(1024)
            if ack.decode() == "ACK":
                ack_received = True
                print("Mensaje enviado correctamente.")
        except socket.timeout:
            attempts += 1
            print(f"Reintentando envío del mensaje... {attempts}/{MAX_ATTEMPTS}")

    if not ack_received:
        print("Fallo al enviar el mensaje después de varios intentos.")

# Funcion para recibir datos
def recibir(sock):
    try:
        data, addr = sock.recvfrom(1024)
        sock.sendto("ACK".encode(), addr)
        return data.decode()
    except socket.timeout:
        print("Tiempo de espera agotado, no se recibió el mensaje.")
        return None

# Funcion para cerrar la conexion
def terminar(sock):
    sock.close()
    print("Conexión cerrada.")