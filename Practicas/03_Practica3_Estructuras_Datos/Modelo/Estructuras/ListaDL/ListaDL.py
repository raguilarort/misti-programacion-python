class NodoDoble:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListaDoblementeLigada:
    def __init__(self):
        self.cabeza = None  # Primer nodo
        self.cola = None    # Último nodo

    def insertar_inicio(self, valor):
        nuevo = NodoDoble(valor)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo

    def insertar_final(self, valor):
        nuevo = NodoDoble(valor)
        if not self.cola:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo

    def eliminar_inicio(self):
        if not self.cabeza:
            print("La lista está vacía.")
            return None
        valor = self.cabeza.valor
        self.cabeza = self.cabeza.siguiente
        if self.cabeza:
            self.cabeza.anterior = None
        else:
            self.cola = None
        return valor

    def eliminar_final(self):
        if not self.cola:
            print("La lista está vacía.")
            return None
        valor = self.cola.valor
        self.cola = self.cola.anterior
        if self.cola:
            self.cola.siguiente = None
        else:
            self.cabeza = None
        return valor

    def mostrar_adelante(self):
        actual = self.cabeza
        print("Lista adelante:", end=" ")
        while actual:
            print(actual.valor, end=" <-> ")
            actual = actual.siguiente
        print("None")

    def mostrar_atras(self):
        actual = self.cola
        print("Lista atrás:", end=" ")
        while actual:
            print(actual.valor, end=" <-> ")
            actual = actual.anterior
        print("None")