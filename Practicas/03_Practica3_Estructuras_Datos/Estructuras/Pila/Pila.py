#!/usr/bin/env python
# coding: utf-8

# In[5]:
class Pila:
    def __init__(self):#método constructor que se ejecuta cuando se crea un objeto de la clase 
        self.elementos = []#se inicializa una lista vacía que actuará como la pila
    
    def insertar(self, numero):#método que recibirá solo enteros
        self.elementos.append(numero)  #inserta el nuevo número sin ordenar .append para gregar los numeros a la pila
    
    def mostrar(self):#método que es para imprimir
        print("Pila actual:", self.elementos)

# In[ ]:




