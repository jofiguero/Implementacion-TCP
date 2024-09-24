from CHAT_TCP import conectar, enviar, terminar, enviar_mensaje, conectar_vieja

def cliente(direccion, puerto):
    sock = conectar(direccion, puerto)

    # Enviar un mensaje al servidor
    mensaje = input("Escribe un mensaje para enviar al servidor: ")
    enviar_mensaje(direccion, puerto, mensaje)
    #enviar(sock, mensaje)

    # Finalizar conexión
    terminar(sock)

if __name__ == "__main__":
    direccion_servidor = "127.0.0.1"  # Dirección local para pruebas
    puerto_servidor = 12345  # El mismo puerto que usa el servidor

    cliente(direccion_servidor, puerto_servidor)  # Invocar la función principal del cliente
