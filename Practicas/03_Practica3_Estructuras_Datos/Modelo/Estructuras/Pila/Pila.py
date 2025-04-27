#!/usr/bin/env python
# coding: utf-8

# In[5]:
class Nodo:#clase que representará un nodo en la pila. cada nodo contendrá un valor y un puntero al siguiente nodo en la pila
    def __init__(self, valor):
        self.valor = valor  #asigna el valor recibido al atributo valor del nodo. Este valor es lo que almacenará el nodo
        self.siguiente = None  #inicializa el atributo siguiente como None. este atributo actuará como un puntero al siguiente nodo en la pila. al principio, no hay otro nodo, por lo que se establece como None

class Pila:#esta clase manejará la estructura de la pila utilizando nodos
    def __init__(self):#constructor de la clase
        self.tope = None  #inicializa la pila vacía
    
    def insertar(self, numero):#metodo para insertar elementos push. recibe un numero como argumento
        nuevo_nodo = Nodo(numero)  #crea un nuevo nodo con el numero ingresado
        nuevo_nodo.siguiente = self.tope  #el siguiente nodo del nuevo nodo será el nodo que estaba en el tope
        self.tope = nuevo_nodo  #actualiza el atributo tope de la pila para que apunte al nuevo nodo
    
    def mostrar(self):
        if not self.tope:#verifica si la pila está vacía
            print("La pila está vacía.")
        else:
            nodo_actual = self.tope
            print("Pila actual:", end=" ")#end=" " para asegurar que los valores se impriman en una sola línea
            while nodo_actual:#bucle que recorrera toda la pila
                print(nodo_actual.valor, end=" ")
                nodo_actual = nodo_actual.siguiente
            print() 
    
    def pop(self):
        if self.tope:#verifica si la pila no esta vacía
            valor_eliminado = self.tope.valor  #guardamos el valor del nodo a eliminar
            self.tope = self.tope.siguiente  #actualiza el atributo tope para que apunte al siguiente nodo, eliminando efectivamente el nodo actual del tope de la pila
            return valor_eliminado
        else:
            print("La pila está vacía.")
            return None

# In[ ]:



