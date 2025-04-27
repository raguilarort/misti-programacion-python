from Modelo.Nodos.Nodo import Nodo

class Pila:#esta clase manejará la estructura de la pila utilizando nodos
    def __init__(self):#constructor de la clase
        self.tope = None  #inicializa la pila vacía
    
    def insertar(self, numero):#metodo para insertar elementos push. recibe un numero como argumento
        nuevo_nodo = Nodo(numero)  #crea un nuevo nodo con el numero ingresado
        nuevo_nodo.right = self.tope  #el siguiente nodo del nuevo nodo será el nodo que estaba en el tope
        self.tope = nuevo_nodo  #actualiza el atributo tope de la pila para que apunte al nuevo nodo
    
    def mostrar(self):
        if not self.tope:#verifica si la pila está vacía
            print("La pila está vacía.")
        else:
            nodo_actual = self.tope
            print("Pila actual:", end=" ")#end=" " para asegurar que los valores se impriman en una sola línea
            while nodo_actual:#bucle que recorrera toda la pila
                print(nodo_actual.value, end=" ")
                nodo_actual = nodo_actual.right
            print() 
    
    def pop(self):
        if self.tope:#verifica si la pila no esta vacía
            valor_eliminado = self.tope.value  #guardamos el valor del nodo a eliminar
            self.tope = self.tope.right  #actualiza el atributo tope para que apunte al siguiente nodo, eliminando efectivamente el nodo actual del tope de la pila
            return valor_eliminado
        else:
            print("La pila está vacía.")
            return None




