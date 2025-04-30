from Modelo.Estructuras.Listas.Lista import Lista
from Modelo.Nodos.Nodo import Nodo

class NodoDoble(Nodo):
    def __init__(self, valor, siguiente=None, anterior=None):
        super().__init__(valor)
        self.siguiente = siguiente
        self.anterior = anterior  
    def __str__(self):
        return f"Nodo doble con valor: {self.valor}"

class ListaDoble(Lista):
    def __init__(self):
        super().__init__()
    
    def insertar(self, v):
        if self.esta_vacia() or self.cabeza.valor > v:
            nuevo = NodoDoble(v, self.cabeza)
            if not self.esta_vacia():
                self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente and actual.siguiente.valor <= v:
                actual = actual.siguiente
            nuevo = NodoDoble(v, actual.siguiente, actual)
            actual.siguiente = nuevo
            if nuevo.siguiente:
                nuevo.siguiente.anterior = nuevo
    
    def borrar(self, v):
        nodo = self.cabeza
        while nodo and nodo.valor != v:
            nodo = nodo.siguiente
        
        if not nodo or nodo.valor != v:
            return
        
        if nodo.anterior:
            nodo.anterior.siguiente = nodo.siguiente
        else:
            self.cabeza = nodo.siguiente
        
        if nodo.siguiente:
            nodo.siguiente.anterior = nodo.anterior
    
    def mostrar(self):
        self._ir_primero()
        nodo = self.cabeza
        while nodo:
            print(f"<- {nodo.valor} -> ", end="")
            nodo = nodo.siguiente
        print()
    
    def _mostrar_descendente(self):
        if self.esta_vacia():
            return
        
        # Ir al último nodo
        nodo = self.cabeza
        while nodo.siguiente:
            nodo = nodo.siguiente
        
        # Mostrar desde el último al primero
        while nodo:
            print(f"<- {nodo.valor} -> ", end="")
            nodo = nodo.anterior
        print()
    
    def _ir_primero(self):
        if self.cabeza:
            while self.cabeza.anterior:
                self.cabeza = self.cabeza.anterior
    
    def _ir_ultimo(self):
        if self.cabeza:
            while self.cabeza.siguiente:
                self.cabeza = self.cabeza.siguiente
    
    def siguiente(self):
        if self.cabeza and self.cabeza.siguiente:
            self.cabeza = self.cabeza.siguiente
            return True
        return False
    
    def anterior(self):
        if self.cabeza and self.cabeza.anterior:
            self.cabeza = self.cabeza.anterior
            return True
        return False
    
    def valor_actual(self):
        return self.cabeza.valor if self.cabeza else None
    
    def buscar(self, v):
        nodo = self.cabeza
        while nodo:
            if nodo.valor == v:
                return True
            nodo = nodo.siguiente
        return False
    
    def modificar(self, viejo, nuevo):
        nodo = self.cabeza
        while nodo:
            if nodo.valor == viejo:
                nodo.valor = nuevo
                return True
            nodo = nodo.siguiente
        return False