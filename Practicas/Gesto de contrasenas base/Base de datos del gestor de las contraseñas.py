import sqlite3
import re

# Conexión a la base de datos (se crea si no existe)
def conectar_bd():
    conexion = sqlite3.connect("gestor_contraseñas.db")
    cursor = conexion.cursor()
    
    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contraseñas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sitio TEXT NOT NULL,
            usuario TEXT,
            email TEXT NOT NULL,
            contraseña TEXT NOT NULL
        )
    ''')
    conexion.commit()
    return conexion, cursor

# --- Funciones para Playfair ---
def preparar_texto(texto):
    # Eliminar espacios y caracteres no alfabéticos, convertir a mayúsculas
    texto = re.sub(r'[^A-Za-z]', '', texto).upper()
    # Reemplazar 'J' por 'I' (común en Playfair)
    texto = texto.replace('J', 'I')
    # Si hay letras repetidas seguidas, insertar 'X' entre ellas
    texto_preparado = []
    for i in range(len(texto)):
        if i > 0 and texto[i] == texto[i-1]:
            texto_preparado.append('X')
        texto_preparado.append(texto[i])
    # Si la longitud es impar, agregar 'X' al final
    if len(texto_preparado) % 2 != 0:
        texto_preparado.append('X')
    return ''.join(texto_preparado)

def generar_matriz(clave):
    clave = preparar_texto(clave)
    alfabeto = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Excluye 'J'
    matriz = []
    # Agregar clave sin repetir letras
    for letra in clave:
        if letra not in matriz and letra in alfabeto:
            matriz.append(letra)
    # Completar con el resto del alfabeto
    for letra in alfabeto:
        if letra not in matriz:
            matriz.append(letra)
    # Convertir a matriz 5x5
    return [matriz[i*5:(i+1)*5] for i in range(5)]

def encontrar_posicion(matriz, letra):
    for fila in range(5):
        for col in range(5):
            if matriz[fila][col] == letra:
                return fila, col
    raise ValueError(f"Letra no encontrada: {letra}")

def cifrar_playfair(texto, clave):
    texto = preparar_texto(texto)
    matriz = generar_matriz(clave)
    texto_cifrado = []
    for i in range(0, len(texto), 2):
        letra1, letra2 = texto[i], texto[i+1]
        fila1, col1 = encontrar_posicion(matriz, letra1)
        fila2, col2 = encontrar_posicion(matriz, letra2)
        # Misma fila: desplazar a la derecha
        if fila1 == fila2:
            texto_cifrado.append(matriz[fila1][(col1 + 1) % 5])
            texto_cifrado.append(matriz[fila2][(col2 + 1) % 5])
        # Misma columna: desplazar hacia abajo
        elif col1 == col2:
            texto_cifrado.append(matriz[(fila1 + 1) % 5][col1])
            texto_cifrado.append(matriz[(fila2 + 1) % 5][col2])
        # Rectángulo: esquinas opuestas
        else:
            texto_cifrado.append(matriz[fila1][col2])
            texto_cifrado.append(matriz[fila2][col1])
    return ''.join(texto_cifrado)

def descifrar_playfair(texto_cifrado, clave):
    matriz = generar_matriz(clave)
    texto_descifrado = []
    for i in range(0, len(texto_cifrado), 2):
        letra1, letra2 = texto_cifrado[i], texto_cifrado[i+1]
        fila1, col1 = encontrar_posicion(matriz, letra1)
        fila2, col2 = encontrar_posicion(matriz, letra2)
        # Misma fila: desplazar a la izquierda
        if fila1 == fila2:
            texto_descifrado.append(matriz[fila1][(col1 - 1) % 5])
            texto_descifrado.append(matriz[fila2][(col2 - 1) % 5])
        # Misma columna: desplazar hacia arriba
        elif col1 == col2:
            texto_descifrado.append(matriz[(fila1 - 1) % 5][col1])
            texto_descifrado.append(matriz[(fila2 - 1) % 5][col2])
        # Rectángulo: esquinas opuestas
        else:
            texto_descifrado.append(matriz[fila1][col2])
            texto_descifrado.append(matriz[fila2][col1])
    return ''.join(texto_descifrado)

def validar_email(email):
    # Patrón para un email básico (ej: nombre@dominio.com)
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def agregar_contraseña():
    print("\nIngresar Datos del Sitio")
    sitio = input("Introduce el sitio web: ")
    email = input("Introduce el correo electronico: ").strip()
    
    while not validar_email(email):
        print("¡Formato del correo electronico inválido! Ejemplo: usuario@dominio.com")
        email = input("Introduce el correo electronico: ").strip()
    
    # Validar que el email no esté vacío
    while not email:
        print("¡El correo electronico no puede estar vacío!")
        email = input("Introduce el correo electronico: ").strip()
    
    # Preguntar si el email es también el usuario
    usar_email_como_usuario = input("¿El usuario es el correo electronico? (si/no): ").lower().strip()
    
    if usar_email_como_usuario == 'si':
        usuario = None  # Indicamos que el usuario es el email
    else:
        usuario = input("Introduce el usuario: ").strip()
        # Validar que el usuario no esté vacío si no se usa el email
        while not usuario:
            print("¡El usuario no puede estar vacío!")
            usuario = input("Usuario: ").strip()
    
    contraseña = input("Introduce el password: ")
    clave_playfair = 'joseprt'
    contraseña_cifrada = cifrar_playfair(contraseña, clave_playfair)
    
    conexion, cursor = conectar_bd()
    cursor.execute(
        "INSERT INTO contraseñas (sitio, usuario, email, contraseña) VALUES (?, ?, ?, ?)",
        (sitio, usuario, email, contraseña_cifrada)
    )
    conexion.commit()
    print("\n¡Datos guardados exitosamente!")
    conexion.close()
    
def ver_contraseñas():
    while True:
        print("\n--- Menú de Visualización ---")
        print("1. Ver todos los sitios web")
        print("2. Buscar un sitio específico")
        print("3. Ver sitios con el mismo email")
        print("4. Regresar al menú principal")
        
        opcion = input("\nSeleccione una opción (1-4): ")
        
        if opcion == "1":
            ver_todos_los_sitios()
        elif opcion == "2":
            buscar_sitio_especifico()
        elif opcion == "3":
            ver_sitios_por_email()
        elif opcion == "4":
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")

def ver_todos_los_sitios():
    conexion, cursor = conectar_bd()   
    cursor.execute("SELECT id, sitio, usuario, email, contraseña FROM contraseñas")
    contraseñas = cursor.fetchall()
    
    if not contraseñas:
        print("\nNo hay contraseñas guardadas.")
    else:
        print("\n--- Todos los sitios ---")
        for id_, sitio, usuario, email, contraseña_cifrada in contraseñas:
            print(f"\nID: {id_} | Sitio: {sitio}")
            print(f"Email: {email}")
            if usuario:
                print(f"Usuario: {usuario}")
            print(f"Contraseña: {contraseña_cifrada}")
                
    conexion.close()

def buscar_sitio_especifico():
    nombre_sitio = input("\nIngrese el nombre del sitio a buscar: ")
    conexion, cursor = conectar_bd()
    cursor.execute("SELECT id, sitio, usuario, email, contraseña FROM contraseñas WHERE sitio LIKE ?", (f"%{nombre_sitio}%",))
    resultados = cursor.fetchall()
    
    if not resultados:
        print("\nNo se encontraron coincidencias.")
    else:
        print("\n--- Resultados de búsqueda ---")
        for id_, sitio, usuario, email, contraseña_cifrada in resultados:
            print(f"\nID: {id_} | Sitio: {sitio}")
            print(f"Email: {email}")
            if usuario:
                print(f"Usuario: {usuario}")
            print(f"Contraseña: {contraseña_cifrada}")

    conexion.close()

def ver_sitios_por_email():
    email_buscar = input("\nIngrese el correo electronico a buscar: ")
    conexion, cursor = conectar_bd()
    cursor.execute("SELECT id, sitio, usuario, contraseña FROM contraseñas WHERE email = ?", (email_buscar,))
    resultados = cursor.fetchall()
    
    if not resultados:
        print(f"\nNo hay sitios registrados con el correo electronico {email_buscar}")
    else:
        print(f"\n--- Sitios con el correo electronico {email_buscar} ---")
        for id_, sitio, usuario, contraseña_cifrada in resultados:
            print(f"\nID: {id_} | Sitio: {sitio}")
            if usuario:
                print(f"Usuario: {usuario}")
            print(f"Contraseña: {contraseña_cifrada}")
    
    conexion.close()

def contraseña_des():
    clave_playfair = 'joseprt'
    conexion, cursor = conectar_bd()
    cursor.execute("SELECT id, sitio, usuario, email, contraseña FROM contraseñas")
    contraseñas = cursor.fetchall()
    
    for id_, sitio, usuario, email, contraseña_cifrada in contraseñas:
        try:
                contraseña_descifrada = descifrar_playfair(contraseña_cifrada, clave_playfair)
                print(f"Contraseña: {contraseña_descifrada}")
        except ValueError as e:
                print(f"¡Error al descifrar! Clave incorrecta o datos corruptos.")
    
    conexion.close()

def actualizar_registro():
    # Mostrar solo sitios web (sin contraseñas/emails)
    conexion, cursor = conectar_bd()
    cursor.execute("SELECT id, sitio FROM contraseñas")
    sitios = cursor.fetchall()
    conexion.close()
    
    if not sitios:
        print("\nNo hay sitios registrados.")
        return
    
    print("\n--- Sitios disponibles ---")
    for id_, sitio in sitios:
        print(f"ID: {id_} | Sitio: {sitio}")
    
    # Seleccionar ID
    id_ = input("\nIngresa el ID del sitio a actualizar: ")
    
    # Mostrar campos editables
    print("\n¿Qué datos deseas actualizar?")
    print("1. Sitio web")
    print("2. Usuario")
    print("3. Correo Electronico")
    print("4. Password")
    opcion = input("Opción: ")
    
    conexion, cursor = conectar_bd()
    
    try:
        if opcion == "1":
            nuevo_valor = input("Nuevo sitio web: ")
            cursor.execute("UPDATE contraseñas SET sitio = ? WHERE id = ?", (nuevo_valor, id_))
        elif opcion == "2":
            nuevo_valor = input("Nuevo usuario: ")
            cursor.execute("UPDATE contraseñas SET usuario = ? WHERE id = ?", (nuevo_valor, id_))
        elif opcion == "3":
            nuevo_valor = input("Nuevo correo electronico: ")
            while not validar_email(nuevo_valor):  # Validar formato email
                print("¡Formato inválido! Ejemplo: usuario@dominio.com")
                nuevo_valor = input("Nuevo correo electronico: ")
            cursor.execute("UPDATE contraseñas SET email = ? WHERE id = ?", (nuevo_valor, id_))
        elif opcion == "4":
            nueva_contraseña = input("Nuevo password: ")
            clave_playfair = "joseprt"
            nueva_contraseña_cifrada = cifrar_playfair(nueva_contraseña, clave_playfair)
            cursor.execute(
                "UPDATE contraseñas SET contraseña = ? WHERE id = ?",
                (nueva_contraseña_cifrada, id_)
            )
        else:
            print("\nOpción no válida.")
            return
        
        conexion.commit()
        print("\n¡Datos actualizados exitosamente!")
        
    except sqlite3.Error as e:
        print(f"\nError al actualizar: {e}")
    finally:
        conexion.close()
        


def eliminar_contraseña():
    # Mostrar solo sitios web 
    conexion, cursor = conectar_bd()
    cursor.execute("SELECT id, sitio FROM contraseñas")
    sitios = cursor.fetchall()
    
    if not sitios:
        print("\nNo hay contraseñas guardadas.")
        conexion.close()
        return
    
    print("\n--- Sitios disponibles ---")
    for id_, sitio in sitios:
        print(f"ID: {id_} | Sitio: {sitio}")
    
    # Pedir ID a eliminar
    try:
        id_ = input("\nIngresa el ID del sitio a eliminar: ")
        
        # Validar que el ID exista
        cursor.execute("SELECT COUNT(*) FROM contraseñas WHERE id = ?", (id_,))
        if cursor.fetchone()[0] == 0:
            print("\n¡Error: ID no válido!")
            return
    
        cursor.execute("DELETE FROM contraseñas WHERE id = ?", (id_,))
        conexion.commit()
        print("\n¡Contraseña eliminada exitosamente!")
        
    except sqlite3.Error as e:
        print(f"\nError al eliminar: {e}")
    finally:
        conexion.close()

def menu():
    while True:
        print("\n=== Gestor de Contraseñas para sitios web===")
        print("1. Ingresar Datos del Sitio")
        print("2. Imprimir Datos del Sitio")
        print("3. Eliminar Sitio")
        print("4. Cambiar Datos del Sitio")
        print("5. Recuperar clave del Sitio")
        print("0. Salir del programa")
        
        opcion = input("\nOpción: ")
        
        if opcion == "1":
            agregar_contraseña()
        elif opcion == "2":
            ver_contraseñas()
        elif opcion == "3":
            eliminar_contraseña()
        elif opcion == "4":
            actualizar_registro()
        elif opcion == "5":
            contraseña_des()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Intenta de nuevo.")

# Ejecutar el programa
if __name__ == "__main__":
    menu()