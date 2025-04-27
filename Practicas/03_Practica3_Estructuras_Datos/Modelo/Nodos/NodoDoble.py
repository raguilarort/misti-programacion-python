
import Nodo
'''
Clase que representa un nodo doble
'''
class NodoDoble(Nodo):
    def __init__(self, valor):
        super().__init__(valor)
        self.left = None

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, nodo):
        self._left = nodo

    def __str__(self):
        return f"Nodo doble con valores: {super().__str__}, Left: {self.left}"