import platform
import os
import time

from Estructuras.Lista_Simple.Pra3 import ListaSimple
from Estructuras.Cola.Cola import Cola
from Estructuras.Pila.Pila import Pila
from Estructuras.ListaDL import ListaDoblementeLigada

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

def menu_lista_simple(lista):
    while True:
        print("\nOperaciones de Lista Simple:")
        print("1. Insertar")
        print("2. Modificar")
        print("3. Mostrar")
        print("4. Borrar")
        print("5. Borrar lista")
        print("0. Regresar al menú principal")

        opcion = input("Ingresa tu opción: ")

        if opcion == "1":
            try:#try-except para manejar cualquier error por un valor inválido
                numero = int(input("Ingresa un número entero a insertar en la lista simple: "))
                print(lista.insertar(numero))
                print("Número insertado correctamente.")
            except ValueError:
                print("Por favor, ingresa solo números enteros.")
        elif opcion == "2":
            lista.modificar()
        elif opcion == "3":
            lista.mostrar()
        elif opcion == "4":
            try:#try-except para manejar cualquier error por un valor inválido
                numero = int(input("Introduzca el número a borrar: "))
                if lista.buscar(numero):
                    lista.borrar(numero)
                else:
                    print("El número ingresado ",{numero},", no existe en la lista.")
            except ValueError:
                print("Por favor, ingresa solo números enteros.")
        elif opcion == "5":
            lista.borrar_lista()
            print("La lista se eliminó.")         
        elif opcion == "0":
            break
        else:
            print("Opción no válida")


def menu_pila(pila):  #función para mostrar el menú y gestionar las operaciones de la pila
    while True:
        print("\n1. Push (Insertar)")
        print("2. Mostrar pila")
        print("3. Pop (Eliminar)")
        print("0. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":  #insertar elemento en la pila
            try:
                numero = int(input("Ingresa un número entero: "))
                pila.insertar(numero)  #se llama a pila.insertar para guardar el número ingresado
                print("Número insertado correctamente.")
            except ValueError:
                print("Por favor, ingresa solo números enteros.")
        elif opcion == "2":  #mostrar la pila actual
            pila.mostrar()
        elif opcion == "3":  #eliminar elemento de la pila
            elemento_eliminado = pila.pop()  #llamar al método pop de la pila
            if elemento_eliminado is not None:
                print(f"Elemento eliminado: {elemento_eliminado}")
            else:
                print("La pila está vacía, no se puede eliminar ningún elemento.")
        elif opcion == "0":  #salir del menú de la pila
            print("Saliendo del programa...")
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
        print("4. Mostrar contenido")
        print("0. Regresar al menú principal")

        opcion = input("Ingresa tu opción: ")

        if opcion == "1":
            try:
                numero = int(input("Ingresa un número entero: "))
                cola.encolar(numero) #Se llama la funcion encolar para agregar el numero recibido
            except ValueError:
                print("Por favor, ingresa solo números enteros.")
        elif opcion == "2":
            elemento = cola.desencolar()

            if elemento:
                print("Elemento desencolado:", elemento.valor)
            else:
                print("La cola está vacía, no hay elementos para extraer.")
        elif opcion == "3":
            print("Tamaño de la cola:", cola.tamanio())
        elif opcion == "4":
            cola.mostrar_elementos()
        elif opcion == "0":
            break
        else:
            print("Opción no válida")
        
        time.sleep(3)
        
def menu_lista_doblemente_ligada(lista):
    while True:
        print("\n1. Insertar al inicio")
        print("2. Insertar al final")
        print("3. Eliminar del inicio")
        print("4. Eliminar del final")
        print("5. Mostrar desde el inicio")
        print("6. Mostrar desde el final")
        print("0. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            valor = input("Ingresa un valor: ")
            lista.insertar_inicio(valor)
        elif opcion == "2":
            valor = input("Ingresa un valor: ")
            lista.insertar_final(valor)
        elif opcion == "3":
            eliminado = lista.eliminar_inicio()
            if eliminado is not None:
                print(f"Elemento eliminado: {eliminado}")
        elif opcion == "4":
            eliminado = lista.eliminar_final()
            if eliminado is not None:
                print(f"Elemento eliminado: {eliminado}")
        elif opcion == "5":
            lista.mostrar_adelante()
        elif opcion == "6":
            lista.mostrar_atras()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


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
                    lista = ListaSimple()
                    print("Esta es la lista")
                    print(lista)
                    menu_lista_simple(lista)
                case 2:
                    #Lista circular
                    pass
                case 3:
                    pila = Pila()
                    menu_pila(pila)#llamamos la funcion menu para ejecutar el programa                    
                case 4:
                    cola = Cola()
                    menu_cola(cola)
                case 5:
                    #Lista doblemente ligada
                    lista = ListaDoblementeLigada()
                    menu_lista_doblemente_ligada(lista)
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
