import socket
from CHAT_TCP import conectar, recibir, terminar

def servidor(puerto):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', puerto))  # Escuchar en cualquier direccion

    print(f"Servidor escuchando en el puerto {puerto}")

    # Esperar handshaking (SYN)
    while True:
        data, addr = udp_socket.recvfrom(1024)
        if data.decode() == "SYN":
            print("SYN recibido, enviando SYN-ACK...")
            udp_socket.sendto("SYN-ACK".encode(), addr)
            break

    # Esperar ACK final del handshaking
    data, addr = udp_socket.recvfrom(1024)
    if data.decode() == "ACK":
        print("Conexion establecida con el cliente", addr)

    while True:
        data, addr = udp_socket.recvfrom(1024)
        print(data.decode())


if __name__ == "__main__":
    puerto_servidor = 12345  # Define el puerto en el que va a escuchar el servidor
    servidor(puerto_servidor)  # Invocar la funcion principal del servidor
