from Estructuras.Cola.Nodo import Nodo

class Cola:
    def __init__(self):
        self.primero = None #Se inicializa la lista con el apuntador al primer elemento limpio
        self.ultimo = None #Se inicializa la lista con el apuntador al último elemento limpio

    #Método que inserta elementos a la cola
    def encolar(self, v):
        nuevo_nodo = Nodo(v) #Se crea el nuevo nodo con el valor indicado por el usuario

        if self.esta_vacia(): #Si la cola está vacía entonces ambos apuntadores apuntan al mismo nodo
            self.ultimo = nuevo_nodo
            self.primero = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo #El último nodo de la cola apuntará al nuevo y el nuevo apuntará a NULL
            self.ultimo = nuevo_nodo #El apuntador del último elemento apuntará al nuevo nodo que se agregó

    def desencolar(self):
        if self.esta_vacia(): #Si la cola está vacía entonces ambos apuntadores apuntan al mismo nodo
            return None
        else:
            nodo = self.primero
            self.primero = nodo.siguiente

            if self.primero == None : self.ultimo = None

            return nodo

    #Método que permite identificar si la cola está vacía
    def esta_vacia(self):
        if self.primero == None and self.ultimo == None:
            return True
        else:
            return False
    
    #Método que devuelve el tamaño de la cola
    def tamanio(self):
        tamanio = 0

        nodo_actual = self.primero

        while nodo_actual:
            tamanio += 1
            nodo_actual = nodo_actual.siguiente
        
        return tamanio
        
    def mostrar_elementos(self):
        if self.esta_vacia():
            print("Cola vacía")
        else:
            nodo_actual = self.primero

            while nodo_actual:
                print(f"{nodo_actual.valor} -> ", end="")
                nodo_actual = nodo_actual.siguiente

            print("NULL")

    def mostrar_primer_elemento(self):
        print(f"{self.primero.valor}")

    def mostrar_ultimo_elemento(self):
        print(f"{self.ultimo.valor}")
