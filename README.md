# Readme Tarea 2, Joaquin Figueroa Mora, 21.262.773-9

## Desiciones de diseño
- Para representar un mensaje tcp se optó por construir una clase __Mensaje_TCP__ para lograr una modularizacion de los datos necesarios y un acceso mas directo y sencillo a sus atributos. Al ser una clase, no era posible enviarlo via socket.send() por lo que se usó la clasica función __str__ para construir una version atomizada y parseable de el mensaje, cuyos atributos eran separados por el caracter "|". Para enviar un mensaje, antes de codificarlo se transformaba a string, y al recibir un mensaje se usa la funcion parsear_tcp() que toma el string y retorna una instancia de __Mensaje_TCP__ equivalente.

- Se decidió optar por que la funcion recibir(mensaje,socket) tuviera una firma tal que en vez de recibir un string para colocar el mensaje, recibiera unicamente el socket y el mensaje fuese el retorno de la funcion.

- Para simplificar la implementación se optó por manejar los tamaños de envio y recepcion en caracteres y no en bytes, de modo que cada segmento de una ventana tiene a lo más 100 caracteres de contenido en mensaje, a lo que hay que sumarle lo que ocupan en espacio los atributos de cabecera. Como el  tamaño de cada segmento es pequeño (aproximadamente 100 bytes por mensaje), **enviar un archivo de texto muy grande podría demorar mucho tiempo**.

- No se implementó un ack_number pues no fue necesario, bastó con utlizar el numero de secuencia dado que no se enviaría informacion extra en un mensaje de ack y por ende un mensaje de confirmacion cumple unicamente este proposito. En su reemplazo, se reutilizó el numero de secuencia o "seq" para chequear cual era el mensaje cuya recepcion estaba siendo confirmada.

- Se optó por situar una ventana de envio en el emisor, al estilo Go-back N, pero con la diferencia de que en vez de mover la ventana cada vez que se recibia un mensaje de los primeros de la ventana, se mueve cuando se reciben todos los mensajes de la ventana.

- Para llevar la cuenta de cada mensaje que efectivamente se va recibiendo se creó una lista de booleanos asginados respectivamente a cada mensaje del segmento. Al recibir el primer mensaje de la ventana se usa el atributo total del mismo para que el receptor tenga seguridad de cuantos mensajes le deberían llegar y de esa manera construir la checklist y la lista en la que contendrá los mensajes.

- En la función recibir, luego de haber recibido efectivamente todos los mensajes esperados, se esperan 3 segundos extras por si se recibe nuevamente un mensaje por parte del emisor (lo que significaría que no recibió el ack) y se reenvian los ack necesarios. Esto provoca que un envio de mensajes se demora un minimo de 3 segundos aun si el mensaje es pequeño.

- Dados los tests realizados, se optó por implementar un fairness que suma 3 segmentos al tamaño de la ventana por cada recibimiento exitoso y lo divide por dos por cada timeout ocurrido. Esto fue testeado con un loss de hasta un 40% de los paquetes y resultó ser relativamente rapido (considerando el tamaño de la ventana, si resulta que el archivo con el que se quiere probar es muy grande (> 1 MB), mejor será modificar este valor en la invocación de la funcion dividir mensaje).

## Como ejecutar la tarea

El enunciado de la tarea hacia mención a que será importada para ser probada, en cuyo caso lo unico que se debe hacer es importar las funciones __conectar__, __enviar__, __recibir__ y __finalizar__ en el comienzo del archivo y usarlas dentro del script.

Sin embargo, en caso de que les sirva, me tomé la libertad de hacer dos scripts que facilitan la ejecución y el testing de la tarea para hacerlo mas dinamico y entendible. Para ocuparlos se deben seguir los siguientes pasos:

1) Primero, se deben descargar los archivos de la tarea, en particular los archivos __t2.py__, __Persona1.py__ y __Persona2.py__, todos estos deben quedar en el mismo directorio.

2) Luego, se abren dos terminales y se navega hacia el directorio creado para almacenar los archivos usando el comando cd de la forma:
**´´cd ruta/hacia/directorio**

3) Posteriormente se debe ejecutar el programa Persona2.py en una de las dos terminales, que es quien hace de servidor, para posteriormente ejecutar el programa Persona1.py en la otra terminal, que es quien hace de cliente.

Esto se realiza con los siguientes comandos: 

- python Persona2.py
- python Persona1.py

4) La terminal cliente, consultará si es que se desea enviar un mensaje propio o generar uno predeterminado con un largo especifico, usted podrá escoger entre estas dos opciones:

- La primera alternativa es enviar un mensaje propio, que se deberá escribir o copiar en la consola cliente

- La segunda alternativa es enviar un mensaje generado cuyo largo es definido por usted

Cabe aclarar que la ventana de envío escogida en la tarea es pequeña, razón por la cual un archivo muy grande podría tardar en enviarse, pero eventualmente debería llegar.

5) Si se desea aplicar una simulacion de perdida de paquetes para estudiar si la tarea cumple con ser segura para enviar mensajes, se pueden usar los siguientes comandos en la terminal: 

Para setear una perdida del x% de los paquetes:
sudo tc qdisc add dev lo root netem loss 20%

Para consultar la perdida actual:
tc qdisc show dev lo

Para finalizar la simulacion de perdida:
sudo tc qdisc del dev lo root netem

Este ultimo comando es importante para regresar el computador a la normalidad luego del testing.

Muchas gracias por su tiempo.