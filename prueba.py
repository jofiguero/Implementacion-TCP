from TCP import Mensaje_TCP

def dividir_mensaje(mensaje,maximo):
    return [mensaje[i:i + maximo] for i in range(0, len(mensaje), maximo)]

mensaje = "Lorem ipsum dolor sit amet consectetur adipiscing elit netus justo, nisi venenatis lacus praesent ac mi ornare pellentesque, libero blandit etiam a aliquet placerat conubia cursus. Taciti eget orci varius fusce ultricies dui gravida neque himenaeos curae primis turpis, augue mauris duis per purus laoreet pellentesque ligula condimentum porta."

print(dividir_mensaje(mensaje,5))