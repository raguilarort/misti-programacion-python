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

#from pila import Pila  # Importamos la clase Pila desde pila.py aqui agregar la parte de eliminación
def menu():#función para mostrar el menú y gestionar la inserción
    pila = Pila()#instancia. objeto pila de la clase Pila para almacenar los números ingresados
    while True:#
        print("\n1. Push")
        print("2. Mostrar pila")
        print("3. Salir")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            try:#try-except para manejar cualquier error por un valor inválido
                numero = int(input("Ingresa un número entero: "))
                pila.insertar(numero)#se llama a pila.insertar para guardar el numero ingresado
                print("Número insertado correctamente.")
            except ValueError:
                print("Por favor, ingresa solo números enteros.")
        elif opcion == "2":
            pila.mostrar()
        elif opcion == "3":
            print("Saliendo del programa")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


menu()#llamamos la funcion menu para ejecutar el programa


# In[ ]:




