import socket
import time

"""
Mensaje_TCP: Clase que representa un mensaje TCP y contiene no solo el cuerpo sino tambien todos los atributos
del encabezado que fueron considerados pertinentes para el desarrollo de esta tarea.

mensaje: Es el mensaje propiamente tal
ACK: Es la flag ACK, indica si el mensaje es una confirmacion o no
SYN: Es la flag SYN, indica si el mensaje es una solicitud de sincronizacion
FIN: Es la flag FIN, indica si el mensaje es una solicitud de cierre de conexion
seq: Es el identificador de este mensaje dentro de una ventana mas grande
total: Es el total de mensajes que serán enviados en esta ventana
"""
class Mensaje_TCP:
    def __init__(self, mensaje, ACK, SYN, FIN, seq, total):
        self.mensaje = mensaje
        self.ACK = ACK
        self.SYN = SYN
        self.FIN = FIN
        self.seq = seq
        self.total = total
    
    def __str__(self):
        return f"{self.mensaje}|{self.ACK}|{self.SYN}|{self.FIN}|{self.seq}|{self.total}"

"""
parsear_tcp: string -> Mensaje_TCP

Recibe un string en formato "mensaje|ACK|SYN|FIN|seq|total", lo procesa y transforma en un Mensaje_TCP
"""
def parsear_tcp(string):
    string_spliteado = string.split("|")
    return Mensaje_TCP(string_spliteado[0],int(string_spliteado[1]),int(string_spliteado[2]),int(string_spliteado[3]),int(string_spliteado[4]),int(string_spliteado[5]))

"""
dividir_mensaje: string, int -> array[string]

Recibe un mensaje y un largo maximo de segmento, y divide el mensaje en tantos strings como haga falta de modo que
ninguno de ellos sea mas grande que dicho maximo
"""
def dividir_mensaje(mensaje,maximo):
    return [mensaje[i:i + maximo] for i in range(0, len(mensaje), maximo)]

"""
false_arr: int -> array[bool]

Devuelve un array de False de tamaño n
"""
def false_arr(n):
    arr = []
    for i in range(n):
        arr += [False]
    return arr

"""
none_arr: int -> array[None]

Devuelve un array de None de tamaño n
"""
def none_arr(n):
    arr = []
    for i in range(n):
        arr += [None]
    return arr

"""
check_array: array[bool] -> bool

Revisa si todos los elementos del array están en True
"""
def check_arr(array):
    for j in range(len(array)):
        if array[j] == False:
            return False
    return True

"""
check_array: array[bool], int, int -> bool

Revisa si todos los elementos del array entre los parametros indicados están en True
"""
def check_arr_between(array, desde, hasta):
    for j in range(desde, hasta):
        if array[j] == False:
            return False
    return True


"""
conectar: string, int -> socket

Recibe una direccion y un puerto y crea un socket que conecta a dicha posicion, para esto realiza
el three way handshake estando configurado con un timeout de 1 segundo y por a lo más 30 intentos. 
Luego retorna el socket ya conectado.
"""
def conectar(direccion, puerto):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Fijamos un puerto y una direccion especificas para el socket
    sock.connect((direccion,puerto))

    # Enviamos un mensaje con syn activado
    print("Solicitando conexion")
    sock.settimeout(1.0)
    intentos = 0
    while True:
        sock.send(str(Mensaje_TCP("",0,1,0,0,1)).encode())
        try:
            # Esperamos recibir un mensaje con syn y ack activados
            data = sock.recv(1024)
            mensaje_decodificado = parsear_tcp(data.decode())
            if mensaje_decodificado.SYN == 1 and mensaje_decodificado.ACK == 1:
                print("Recibimos respuesta, confirmamos de vuelta")
                sock.send(str(Mensaje_TCP("",1,0,0,0,1)).encode())
                print("Conexión establecida")
                sock.settimeout(None)
                return sock
        #Si es que se acaba el tiempo
        except socket.timeout:
            intentos += 1
            #Si ya llevamos mas de 30 intentos, 
            if intentos > 30:
                break
            continue

    raise ConnectionError("No se pudo establecer la conexión.")


"""
enviar: socket, string -> void

Recibe un socket ya conectado a algún lugar, y un mensaje, el cual divide en diversos submensajes de tamaño
100 caracteres y los envía en ventanas de un tamaño que va variando conforme se va testeando la red, una vez
enviada la ventana espera los ack de los mensajes y luego prosigue con la siguiente. 
En caso de no recibir todos los ack dentro de su timeout de 1 segundo, los vuelve a enviar todos.
"""
def enviar(sock, mensaje):

    def enviar_ventana(total,mensajes,sock,window_pos,window_size):
        for i in range(window_pos, min(window_pos+window_size,total)):
            segmento = Mensaje_TCP(mensajes[i],0,0,0,i,total)
            sock.send(str(segmento).encode())

    #Dividimos el mensaje en submensajes de tamaño 10
    mensajes = dividir_mensaje(mensaje,100) 
    total = len(mensajes)
    window_size = 1
    window_pos = 0
    #Creamos un array de falsos para saber cuales ack ya hemos recibido
    checklist = false_arr(total)
    #Seteamos un timeout
    sock.settimeout(1.0)
    
    while not check_arr(checklist):
        #Creamos un for que crea un Mensaje_TCP y lo asocia a un elemento de la lista para luego enviarlo
        enviar_ventana(total, mensajes, sock, window_pos, window_size)


        #Esperamos una respuesta
        while not check_arr_between(checklist,window_pos, min(window_pos + window_size, total)):
            try:
                respuesta = parsear_tcp(sock.recv(1024).decode())
                #Si el mensaje es un ACK
                if respuesta.ACK == 1:
                    #Lo marcamos como recibido
                    checklist[respuesta.seq] = True
                    window_size += 3
            #Si se acaba el timeout:
            except socket.timeout:
                if window_size > 2:
                    window_size = int(window_size / 2)
                else:
                    window_size = 1
                enviar_ventana(total,mensajes,sock,window_pos,window_size)

        #Movemos la ventana
        window_pos += window_size
    print("Termine")
    sock.settimeout(None)
    print("Mensaje enviado correctamente.")


"""
recibir: socket -> void

Recibe un socket que ya está conectado a un lugar específico. Escucha para recibir el primer mensaje de todos.
Con este mensaje puede conocer cual es la cantidad total de mensajes que van a venir, con lo cual crea una 
checklist que se va llenando conforme van llegando los mensajes. Una vez se ha enviado el ack del ultimo mensaje
que se estaba esperando, se realiza una ultima espera de 3 seg para comprobar que efectivamente la otra persona haya 
recibido todos los ack, se arma el mensaje final y se retorna.
"""
def recibir(sock):
    #Recibimos algún mensaje
    primera_recepcion = parsear_tcp(sock.recv(1024).decode())

    #Creamos una Checklist para llevar registro de cuales mensajes ya recibimos usando el dato "total"
    checklist = false_arr(primera_recepcion.total)
    # Registramos en la lista el dato recibido (No necesariamente será el primero de la secuencia) y enviamos ack
    checklist[primera_recepcion.seq] = True
    #Creamos una lista de None's para almacenar todos los mensajes recibidos y poder unirlos luego
    mensajes_tcp = none_arr(primera_recepcion.total)
    mensajes_tcp[primera_recepcion.seq] = primera_recepcion
    
    #Le respondemos
    respuesta = Mensaje_TCP("",1,0,0, primera_recepcion.seq, primera_recepcion.total)
    sock.send(str(respuesta).encode())
    

    #Entramos en un bucle de recibir mensajes y enviar ack's 
    sock.settimeout(3.0)
    while(not check_arr(checklist)):
        recibido = parsear_tcp(sock.recv(1024).decode())
        checklist[recibido.seq] = True
        mensajes_tcp[recibido.seq] = recibido
        respuesta = Mensaje_TCP("",1,0,0, recibido.seq, recibido.total)
        sock.send(str(respuesta).encode())
    
    #Verificamos que la otra persona haya recibido todos nuestros ack's
    while True:
        try:
            #Vemos si nos llega un mensaje en tres segundos
            recibido = parsear_tcp(sock.recv(1024).decode())
            #Si nos llega, enviamos un ack para ese mensaje
            respuesta = Mensaje_TCP("",1,0,0, recibido.seq, recibido.total)
            sock.send(str(respuesta).encode())

        #Si no nos llega nada, entonces el cliente tambien recibió todos los ack
        except socket.timeout:
            break
    
    sock.settimeout(None)

    #Una vez que ya recibimos todos los mensajes, armamos el mensaje final y lo retornamos
    mensaje_armado = ""
    for i in range(len(mensajes_tcp)):
        mensaje_armado += mensajes_tcp[i].mensaje
    
    return mensaje_armado

    



"""
terminar: socket -> void

Recibe un socket concetado a una direccion y finaliza la conexion con la otra entidad, para esto realiza
el four way handshake estando configurado con un timeout de 1 segundo y por a lo más 5 intentos (menos que en 
conectar dado que aqui simplemente estamos avisando, no nos importa tanto que el otro sepa, es su responsabilidad). 
"""
def terminar(sock):
    print("Solicitando fin de conexion")
    # Esperamos recibir un mensaje con fin y ack activados
    sock.settimeout(1.0)
    intentos = 0
    while True:
        # Enviamos un mensaje con fin activado
        sock.send(str(Mensaje_TCP("",0,0,1)).encode())
        try: 
            data = sock.recv(1024)
            mensaje_decodificado = parsear_tcp(data.decode())

            if mensaje_decodificado.FIN == 1 and mensaje_decodificado.ACK == 1:
                print("Recibimos respuesta, confirmamos de vuelta")
                sock.send(str(Mensaje_TCP("",1,0,0)).encode())
                print("Conexión finalizada")
                sock.close()
        except socket.timeout:
            intentos += 1
            if intentos > 5:
                break

    #Si realizamos mas de 5 intentos infructuosos, cerramos conexion pues ya hemos dado aviso igualmente
    sock.close()
