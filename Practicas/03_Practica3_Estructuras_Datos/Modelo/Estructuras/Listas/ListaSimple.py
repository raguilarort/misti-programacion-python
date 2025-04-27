from Modelo.Estructuras.Listas.Lista import Lista
from Modelo.Nodos.Nodo import Nodo


class ListaSimple(Lista):
    def __init__(self):
        super().__init__()

    def insertar(self, v):
        if not self.elemento_existente(v):
            nuevo = Nodo(v)        
        
            # Si la lista está vacía o el nuevo valor es menor que el primero
            if self.esta_vacia() or self.cabeza.value > v:
                nuevo.right = self.cabeza
                self.cabeza = nuevo
            else:
                anterior = self.cabeza
                # Buscar la posición de inserción
                while anterior.right and anterior.right.value <= v:
                    anterior = anterior.right
                # Insertar el nuevo nodo
                nuevo.right = anterior.right
                anterior.right = nuevo
            print("Elemento insertado correctamente")
        else:
            print("El elemento no se pudo insertar porque ya existía")
    
    def borrar(self, v):
        actual = self.cabeza
        anterior = None
        
        # Buscar el nodo a borrar
        while actual and actual.value < v:
            anterior = actual
            actual = actual.right
        
        # Si no se encontró el valor
        if not actual or actual.value != v:
            return
        
        # Borrar el nodo
        if anterior is None:  # Es el primer nodo
            self.cabeza = actual.right
        else:
            anterior.right = actual.right
        # En Python no necesitamos free(), el recolector de basura lo maneja
    
    def borrar_lista(self):
        while self.cabeza:
            temp = self.cabeza
            self.cabeza = self.cabeza.right
            temp = None  # Esto ayuda al recolector de basura
    
    def mostrar(self):
        if self.esta_vacia():
            print("Lista vacía")
        else:
            nodo = self.cabeza
            while nodo:
                print(f"{nodo.value} -> ", end="")
                nodo = nodo.right
            print("None")

    def modificar(self):
        mod = int(input('Número a modificar: '))
    
        # Primero verificamos si el número está en la lista
        encontrado = False
        actual = self.cabeza
        while actual:
            if actual.value == mod:
                encontrado = True
                break
            actual = actual.right
    
        if not encontrado:
            print(f"El número {mod} no está en la lista")
            return
    
        # Si llegamos aquí, el número existe en la lista
        self.borrar(mod)
        ins = int(input('Número a insertar: '))
        self.insertar(ins)
    
    '''
    Método para verificar la existencia de un elemento
    '''
    def buscar(self, v):
        if not self.esta_vacia():
            nodo_actual = self.cabeza
            
            while nodo_actual:
                if nodo_actual.value == v:
                    return True
                
                nodo_actual = nodo_actual.right

# Programa principal equivalente al main() en C
'''
if __name__ == "__main__":
    lista = ListaSimple()
    number = int (input('Numero: '))
    lista.insertar(number)

    number = int (input('Numero: '))
    lista.insertar(number)
    lista.insertar(40)
    lista.insertar(30)
    
    lista.mostrar()
    
    lista.borrar(number)
    lista.borrar(15)
    lista.borrar(45)
    lista.borrar(30)
    lista.borrar(40)
    
    lista.mostrar()
    
    lista.borrar_lista()    
    lista.mostrar()
    
    lista.insertar(30)    
    lista.mostrar()
    
    lista.insertar(60)    
    lista.mostrar()
    
    lista.insertar(15)    
    lista.mostrar()
    lista.modificar()    
    lista.mostrar()
'''