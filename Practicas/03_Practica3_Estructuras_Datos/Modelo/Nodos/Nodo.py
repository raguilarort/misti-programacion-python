'''
Clase que representa un nodo simple
'''
class Nodo:
    def __init__(self, v):
        self.value = v #Atributo de instancia que almacena el valor del nodo
        self.right = None #Atributo de instancia que almacena la referencia al nodo de la derecha o siguiente

    #Método que muestra la información que contiene el nodo
    def mostrar_informacion(self):
        print(self.__str__)

    #Método que permite insertar el valor que almacenará el nodo
    def guardar_informacion(self, v):
        self.valor = v

    #Método que permite guardar la referencia al nodo de la derecha o siguiente
    def nuevo_siguiente(self, Nodo):
        self.siguiente = Nodo

    def __str__(self):
        return f"Nodo simple con valores: {self.valor, self.right}"