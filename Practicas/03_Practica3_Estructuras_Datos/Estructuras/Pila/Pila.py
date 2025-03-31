#!/usr/bin/env python
# coding: utf-8

# In[5]:
class Pila:
    def __init__(self):
        self.elementos = []  # Lista vacía que actuará como la pila
    
    def insertar(self, numero):
        self.elementos.append(numero)  # Inserta el número en la pila
    
    def mostrar(self):
        print("Pila actual:", self.elementos)  # Muestra la pila
    
    def pop(self):
        """Método para eliminar el último elemento de la pila"""
        if self.elementos:
            return self.elementos.pop()  # Elimina y devuelve el último elemento
        else:
            print("La pila está vacía.")
            return None

# In[ ]:



