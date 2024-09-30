# Readme Tarea 2, Joaquin Figueroa Mora, 21.262.773-9

## Desiciones de diseño
- Para representar un mensaje tcp se optó por construir una clase __Mensaje_TCP__ para lograr una modularizacion de los datos necesarios y un acceso mas directo y sencillo a sus atributos. Al ser una clase, no era posible enviarlo via socket.send() por lo que se usó la clasica función __str__ para construir una version atomizada y parseable de el mensaje, cuyos atributos eran separados por el caracter "|". Para enviar un mensaje, antes de codificarlo se transformaba a string, y al recibir un mensaje se usa la funcion parsear_tcp() que toma el string y retorna una instancia de __Mensaje_TCP__ equivalente.

- Se decidió optar por que la funcion recibir(mensaje,socket) tuviera una firma tal que en vez de recibir un string para colocar el mensaje, recibiera unicamente el socket y el mensaje fuese el retorno de la funcion.

- Para simplificar la implementación se optó por manejar los tamaños de envio y recepcion en caracteres y no en bytes, de modo que cada segmento de una ventana tiene a lo más 100 caracteres de contenido en mensaje, a lo que hay que sumarle lo que ocupan en espacio los atributos de cabecera. Como el  tamaño de cada segmento es pequeño (aproximadamente 100 bytes por mensaje), **enviar un archivo de texto muy grande podría demorar mucho tiempo**.

- No se implementó un ack_number pues no fue necesario, bastó con utlizar el numero de secuencia dado que no se enviaría informacion extra en un mensaje de ack y por ende un mensaje de confirmacion cumple unicamente este proposito. En su reemplazo, se reutilizó el numero de secuencia o "seq" para chequear cual era el mensaje cuya recepcion estaba siendo confirmada.

- Se optó por situar una ventana de envio en el emisor, al estilo Go-back N, pero con la diferencia de que en vez de mover la ventana cada vez que se recibia un mensaje de los primeros de la ventana, se mueve cuando se reciben todos los mensajes de la ventana.

- Para llevar la cuenta de cada mensaje que efectivamente se va recibiendo se creó una lista de booleanos asginados respectivamente a cada mensaje del segmento. Al recibir el primer mensaje de la ventana se usa el atributo total del mismo para que el receptor tenga seguridad de cuantos mensajes le deberían llegar y de esa manera construir la checklist y la lista en la que contendrá los mensajes.

- En la función recibir, luego de haber recibido efectivamente todos los mensajes esperados, se esperan 3 segundos extras por si se recibe nuevamente un mensaje por parte del emisor (lo que significaría que no recibió el ack) y se reenvian los ack necesarios. Esto provoca que un envio de mensajes se demora un minimo de 3 segundos aun si el mensaje es pequeño.

## Como ejecutar la tarea
