def menu_pila(pila):  # función para mostrar el menú y gestionar las operaciones de la pila
    while True:
        print("\nOperaciones de Pila:")
        print("1. Push (Insertar)")
        print("2. Mostrar pila")
        print("3. Pop (Eliminar)")
        print("4. Buscar elemento")
        print("0. Salir")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":  # Insertar elemento en la pila
            try:
                numero = int(input("Ingresa un número entero: "))
                pila.insertar(numero)  # Se llama a pila.insertar para guardar el número ingresado
                print("Número insertado correctamente.")
            except ValueError:
                print("Por favor, ingresa solo números enteros.")
        elif opcion == "2":  # Mostrar la pila actual
            pila.mostrar()
        elif opcion == "3":  # Eliminar elemento de la pila
            elemento_eliminado = pila.pop()
            if elemento_eliminado is not None:
                print(f"Elemento eliminado: {elemento_eliminado}")
        elif opcion == "4":  # Buscar un elemento en la pila
            try:
                numero = int(input("Ingresa el número a buscar: "))
                if pila.buscar(numero):
                    print(f"El número {numero} se encuentra en la pila.")
                else:
                    print(f"El número {numero} no está en la pila.")
            except ValueError:
                print("Por favor, ingresa solo números enteros.")
        elif opcion == "0":  # Salir del menú
            print("Regresando al menú principal...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")
        