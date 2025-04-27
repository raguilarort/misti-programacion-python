from Estructuras.Arbol_Binario.Nodo import Nodo

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, v):
        if self.raiz is None:
            self.raiz = Nodo(v)
        else:
            self.insertar_recursivo(self.raiz, v)

    def insertar_recursivo(self, nodo_actual, v):
        if v < nodo_actual.dato:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(v)
            else:
                self.insertar_recursivo(nodo_actual.izquierda, v)
        elif v > nodo_actual.dato:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(v)
            else:
                self.insertar_recursivo(nodo_actual.derecha, v)
        else:
            print("El dato ya existe en el árbol.")

    def buscar(self, dato):
        return self.buscar_recursivo(self.raiz, dato)

    def buscar_recursivo(self, nodo_actual, dato):
        if nodo_actual is None:
            return False
        if nodo_actual.dato == dato:
            return True
        if dato < nodo_actual.dato:
            return self.buscar_recursivo(nodo_actual.izquierda, dato)
        return self.buscar_recursivo(nodo_actual.derecha, dato)
    
    def eliminar(self, dato):
        self.raiz = self.eliminar_recursivo(self.raiz, dato)

    def eliminar_recursivo(self, nodo_actual, dato):
        if nodo_actual is None:
            return nodo_actual

        if dato < nodo_actual.dato:
            nodo_actual.izquierda = self.eliminar_recursivo(nodo_actual.izquierda, dato)
        elif dato > nodo_actual.dato:
            nodo_actual.derecha = self.eliminar_recursivo(nodo_actual.derecha, dato)
        else:
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda

            nodo_actual.dato = self.min_valor(nodo_actual.derecha)
            nodo_actual.derecha = self.eliminar_recursivo(nodo_actual.derecha, nodo_actual.dato)
        return nodo_actual
    
    def min_valor(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo.dato

    def imprimir_ordenado(self):
        self.imprimir_ordenado_recursivo(self.raiz)
        print()

    def imprimir_ordenado_recursivo(self, nodo_actual):
        if nodo_actual:
            self.imprimir_ordenado_recursivo(nodo_actual.izquierda)
            print(nodo_actual.dato, end=" ")
            self.imprimir_ordenado_recursivo(nodo_actual.derecha)
