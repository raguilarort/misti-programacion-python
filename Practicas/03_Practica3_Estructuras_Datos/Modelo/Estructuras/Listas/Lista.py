
class Lista:
    def __init__(self):
        self.cabeza = None
    
    #Método que verifica si la lista está vacía
    def esta_vacia(self):
        return self.cabeza is None
    
    #Método que verifica si el elemento que se intenta ingresar ya existe
    def elemento_existente(self, elemento):
        if not self.esta_vacia():
            nodo_actual = self.cabeza
            
            while nodo_actual:
                if nodo_actual.value == elemento:
                    return True
                
                nodo_actual = nodo_actual.right

    #Método que devuelve el tamaño de la lista
    def tamanio(self):
        tamanio = 0

        if self.esta_vacia():
            print("Lista vacía")
        else:
            nodo = self.cabeza
            while nodo:
                tamanio += 1

        return tamanio
    