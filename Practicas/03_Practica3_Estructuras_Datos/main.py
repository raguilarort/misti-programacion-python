import platform
import os
import time

from Estructuras.Cola import Cola
from Estructuras.Pila import Pila

def limpiar_pantalla():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def menu_principal():
        print('******** PRÁTICA 3. ESTRUCTURAS DE DATOS ********\n')
        print('Indica con qué estructura de datos quieres trabajar\n')
        print('1. Lista simple\n')
        print('2. Lista circular\n')
        print('3. Pila\n')
        print('4. Cola\n')
        print('5. Lista doblemente ligada\n')
        print('6. Lista doblemente ligada circular\n')
        print('7. Árbol binario\n')
        print('0. Salir\n')

#from pila import Pila  # Importamos la clase Pila desde pila.py aqui agregar la parte de eliminación
def menu_pila(pila):#función para mostrar el menú y gestionar la inserción
    #pila = Pila()#instancia. objeto pila de la clase Pila para almacenar los números ingresados
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

def menu_cola(cola):
    while True:
        limpiar_pantalla()
        print("\nOperaciones de Cola:")
        print("1. Encolar")
        print("2. Desencolar")
        print("3. Tamaño")
        print("4. Regresar al menú principal")

        opcion = input("Ingresa tu opción: ")

        if opcion == "1":
            item = input("Ingresa el elemento a encolar: ")
            cola.encolar(item)
        elif opcion == "2":
            print("Elemento desencolado:", cola.desencolar())
        elif opcion == "3":
            print("Tamaño de la cola:", cola.tamano())
        elif opcion == "4":
            break
        else:
            print("Opción no válida")



# Función main
def main():
    while True:
        limpiar_pantalla()
        menu_principal()

        try:
            opcion_principal = int(input('Opción: '))

            match opcion_principal:
                case 1:
                    #Lista simple
                    pass
                case 2:
                    #Lista circular
                    pass
                case 3:
                    pila = Pila.Pila()
                    menu_pila(pila)#llamamos la funcion menu para ejecutar el programa                    
                case 4:
                    cola = Cola.Cola()
                    menu_cola(cola)
                    pass
                case 5:
                    #Lista doblemente ligada
                    pass
                case 6:
                    #Lista doblemente ligada Circular
                    pass
                case 7:
                    #Árbol Binario
                    pass
                case 0:
                    print('Cerrando programa...')
                    break
                case _:
                    print('Opción inválida')
                    time.sleep(1)
        except ValueError:
            print("Por favor introduce un valor válido.")
            time.sleep(1)


# Se invoca funcion main()
if __name__ == '__main__':
    main()