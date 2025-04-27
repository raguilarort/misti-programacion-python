class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaSimple:
    def __init__(self):
        self.cabeza = None
    
    def esta_vacia(self):
        return self.cabeza is None
    
    def insertar(self, v):
        nuevo = Nodo(v)
        
        # Si la lista está vacía o el nuevo valor es menor que el primero
        if self.esta_vacia() or self.cabeza.valor > v:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        else:
            anterior = self.cabeza
            # Buscar la posición de inserción
            while anterior.siguiente and anterior.siguiente.valor <= v:
                anterior = anterior.siguiente
            # Insertar el nuevo nodo
            nuevo.siguiente = anterior.siguiente
            anterior.siguiente = nuevo
    
    def borrar(self, v):
        actual = self.cabeza
        anterior = None
        
        # Buscar el nodo a borrar
        while actual and actual.valor < v:
            anterior = actual
            actual = actual.siguiente
        
        # Si no se encontró el valor
        if not actual or actual.valor != v:
            return
        
        # Borrar el nodo
        if anterior is None:  # Es el primer nodo
            self.cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente
        # En Python no necesitamos free(), el recolector de basura lo maneja
    
    def borrar_lista(self):
        while self.cabeza:
            temp = self.cabeza
            self.cabeza = self.cabeza.siguiente
            temp = None  # Esto ayuda al recolector de basura
    
    def mostrar(self):
        if self.esta_vacia():
            print("Lista vacía")
        else:
            nodo = self.cabeza
            while nodo:
                print(f"{nodo.valor} -> ", end="")
                nodo = nodo.siguiente
            print("None")

    def modificar(self):
        mod = int(input('Número a modificar: '))
    
        # Primero verificamos si el número está en la lista
        encontrado = False
        actual = self.cabeza
        while actual:
            if actual.valor == mod:
                encontrado = True
                break
            actual = actual.siguiente
    
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
                if nodo_actual.valor == v:
                    return True
                
                nodo_actual = nodo_actual.siguiente

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