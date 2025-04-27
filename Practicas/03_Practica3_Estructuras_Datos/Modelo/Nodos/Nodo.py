'''
Clase que representa un nodo simple
'''
class Nodo:
    def __init__(self, v):
        self.value = v
        self.right = None

    def mostrar_informacion(self):
        print(self.__str__)

    def guardar_informacion(self, v):
        self.valor = v

    def nuevo_siguiente(self, Nodo):
        self.siguiente = Nodo

    def __str__(self):
        return f"Nodo simple con valores: {self.valor, self.right}"