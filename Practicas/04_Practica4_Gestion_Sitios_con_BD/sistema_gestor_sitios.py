import platform
import os
import time

ALFABETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMERO = 26  # Número de alfabetos
GIRO = len(ALFABETO) // 2 - 1
CLAVE_ALFABETOS = 'PYTHON' #Constante definida para la creación de los tableros

global entrada
global alfabeto
alfabeto = [''] * NUMERO
entrada = [''] * NUMERO

sitios = {} #Se inicializa el diccionario
#sitios['Ticketmaster'] = ('ricardo@ticketmaster.com', 'ricardo@ticketmaster.com', 'LADLWEYOTRMXE', 'yanohayboleto') #boletosgratis
#sitios['Cuevana'] = ('cucu@cuevana.com', 'cucu@cuevana.com', 'MWYXE OAZTMFKSEQ', 'gratis')


def limpiar_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def imprime_sitios(diccionario_sitios, modo):
    limpiar_terminal()
    match modo:
        case "all":
            print("{:^20} {:^30} {:^30} {:^25}".format('Sitio WEB', 'Correo Electrónico', 'Usuario', 'Password Cifrado'))

            for key, value in diccionario_sitios.items():
                email = value[0]
                usuario = value[1]
                password = value[2]
                print("{:<20} {:<30} {:<30} {:<10}".format(key, email, usuario, password))
        case "nombre":
            print("{:^20}".format('Sitio WEB'))

            for key, value in diccionario_sitios.items():
                print("{:<20}".format(key))
    
    print("\n")
    
def imprime_sitio(nombre_sitio, datos_sitio, modo):
    limpiar_terminal()
    match modo:
        case "all":
            print("{:^20} {:^30} {:^30} {:^25}".format('Sitio WEB', 'Correo Electrónico', 'Usuario', 'Password Cifrado'))
            print("{:<20} {:<30} {:<30} {:<10}".format(nombre_sitio, datos_sitio[0], datos_sitio[1], datos_sitio[2]))
        case "nombre":
            print("{:^20}".format('Sitio WEB'))
            print("{:<20}".format(nombre_sitio))

    print("\n")

#Menú principal
def menu_principal():
    print('******** SISTEMA DE GESTIÓN DE SITIOS Y PASSWORDS ********\n')
    print('1. Ingresar Datos del Sitio\n')
    print('2. Cambiar Datos del Sitio\n')
    print('3. Recuperar clave del Sitio\n')
    print('4. Eliminar Sitio\n')
    print('5. Imprimir Datos\n')
    print('8. Salir del Programa\n')

#Menú de opciones para imprimir datos
def menu_opcion2():
    print('\n')
    print('1. Correo Electrónico\n')
    print('2. Usuario\n')
    print('3. Password\n')
    print('0. Regresar al menú anterior\n')

#Menú de opciones para imprimir datos
def menu_opcion5():
    print('Imprimir Datos\n')
    print('1. Todos los sitios web\n')
    print('2. Un sitio web en específico\n')
    print('3. Por correo electrónico\n')
    print('0. Regresar al menú anterior\n')

#Control para agregar nuevos sitios
def control_opcion_1():
    opcion_menu_opcion1 = 0

    limpiar_terminal()

    print('******** OPCION 1 ********\n')
    print('Ingresar Datos del Sitio\n')

    nombre_sitio_web = input('Introduce el sitio WEB: ')
    email_sitio_web = input('Introduce el correo electrónico: ')
    usuario = email_sitio_web
    es_usuario_email = input('¿El usuario es el correo electrónico? (si/no): ').lower().strip() == 'si'

    if es_usuario_email == False:
        usuario = input('Introduce el usuario: ')
    
    password = input('Introduce el password: ').upper()
    llave_cifrado = input('Introduce tu llave para cifrar el password: ').upper()

    criptograma = cifrarMensaje(llave_cifrado, password)

    print('\nSe procede a guardar la información. Por favor espere...\n')
    sitios.update({nombre_sitio_web: (email_sitio_web, usuario, criptograma, llave_cifrado)})
    time.sleep(2)
    print('\nInformación guardada con éxito\n')

#Control para cambiar datos de un sitio (tupla)
def control_opcion_2():
    opcion_menu_opcion2 = 9 #Se inicializa con un valor diferente de 0 porque 0 es regresar al menú anterior

    limpiar_terminal()
       
    print("Cambiar Datos del Sitio")
    imprime_sitios(sitios, modo='nombre')

    sitio_a_buscar = input('Introduce el sitio del que se quiere cambiar datos: ')
                
    sitio_encontrado = sitios.get(sitio_a_buscar)

    if sitio_encontrado != None:
        while opcion_menu_opcion2 != 0:
            menu_opcion2()
            opcion_menu_opcion2 = int(input('Opción: '))

            match opcion_menu_opcion2:
                case 0:
                    break
                case 1:
                    #Opción para cambiar solo el email
                    correo_actual = input('Correo actual: ')

                    sitio_encontrado = sitios.get(sitio_a_buscar) #Traer datos más recientes

                    if correo_actual == sitio_encontrado[0]:
                        correo_nuevo = input('Nuevo correo: ')

                        lista_tmp = list(sitio_encontrado)
                        lista_tmp[0] = correo_nuevo

                        sitios[sitio_a_buscar] = tuple(lista_tmp)

                    else:
                        print("El correo ingresado no coincide con el registro actual. Vuelve a intentarlo.")
                        time.sleep(1)
                    
                case 2:
                    #Opción para cambiar solo el usuario
                    usuario_actual = input('Usuario actual: ')

                    sitio_encontrado = sitios.get(sitio_a_buscar)

                    if usuario_actual == sitio_encontrado[1]:
                        usuario_nuevo = input('Nuevo usuario: ')

                        lista_tmp = list(sitio_encontrado)
                        lista_tmp[1] = usuario_nuevo

                        sitios[sitio_a_buscar] = tuple(lista_tmp)

                    else:
                        print("El usuario ingresado no coincide con el registro actual. Vuelve a intentarlo.")
                        time.sleep(1)

                case 3:
                    #Opción para cambiar solo la contraseña
                    contrasena_actual = input('Contraseña actual: ')

                    sitio_encontrado = sitios.get(sitio_a_buscar)

                    contrasena_descifrada = descifrarMensaje(sitio_encontrado[3].upper(), sitio_encontrado[2].upper())

                    print(contrasena_actual)
                    print(contrasena_descifrada)

                    print(type(contrasena_actual))
                    print(type(contrasena_descifrada))

                    print(len(contrasena_actual))
                    print(len(contrasena_descifrada))

                    print(sitio_encontrado[2])
                    print(sitio_encontrado[3])

                    if contrasena_actual == contrasena_descifrada[:-1]:
                        contrasena_nueva = input('Nueva contraseña: ')

                        lista_tmp = list(sitio_encontrado)
                        
                        criptograma = cifrarMensaje(sitio_encontrado[3].upper(), contrasena_nueva.upper())

                        lista_tmp[2] = criptograma

                        sitios[sitio_a_buscar] = tuple(lista_tmp)

                    else:
                        print("La contraseña ingresada no coincide con el registro actual. Vuelve a intentarlo.")
                        time.sleep(1) 
                            
                case _:
                    print('Opción inválida')
                    time.sleep(1)
    else:
        print("No hay coincidencias con el nombre del sitio ingresado")
        
#Control para recuperar el password
def control_opcion_3():
    limpiar_terminal()
    print("Módulo para recuperar el password del sitio")
    imprime_sitios(sitios, modo='nombre')

    sitio_a_buscar = input('Introduce el sitio del que se quiere obtener el password: ')
                
    sitio_encontrado = sitios.get(sitio_a_buscar)

    if sitio_encontrado != None:

        print("Tu contraseña es: ")
        print(descifrarMensaje(sitio_encontrado[3].upper(), sitio_encontrado[2].upper()))
        #sitio_encontrado[3] es la llave indicada por el usuario
        #sitio_encontrado[2] es el criptograma que se guardó después de cifrar el password
        time.sleep(4)
    else:
        print("No hay coincidencias con el nombre del sitio ingresado")     

#Control para eliminar un sitio
def control_opcion_4():
    limpiar_terminal()
    if bool(sitios):
        print("Eliminar Sitio")
        imprime_sitios(sitios, modo='nombre')
        sitio_a_eliminar = input('Introduce el sitio que deseas eliminar: ')
        
        try:
            del sitios[sitio_a_eliminar]
            print(sitio_a_eliminar + " eliminado correctamente...")
        except KeyError:
            print("El sitio que deseas eliminar no existe")
    else:
        print("El diccionario de sitios está vacío.")

    time.sleep(2)

#Control para mostrar los datos almacenados
def control_opcion_5():
    opcion_menu_opcion5 = 9 #Se inicializa con un valor diferente de 0 porque 0 es regresar al menú anterior

    limpiar_terminal()

    while opcion_menu_opcion5 != 0:        
        menu_opcion5()
        opcion_menu_opcion5 = int(input('Opción: '))

        match opcion_menu_opcion5:
            case 0:
                break
            case 1:
                #Opción para imprimir todos los sitios web
                limpiar_terminal()
                imprime_sitios(sitios, modo='all')
                
            case 2:
                limpiar_terminal()
                imprime_sitios(sitios, modo='nombre')
                sitio_a_buscar = input('Introduce el sitio del que se quiere cambiar datos: ')
                
                sitio_encontrado = sitios.get(sitio_a_buscar)

                if sitio_encontrado != None:
                    imprime_sitio(sitio_a_buscar, sitio_encontrado, modo='all')
                else:
                    print("No hay coincidencias con el nombre del sitio ingresado")               

            case 3:
                limpiar_terminal()
                sitio_a_buscar = input('Introduce el correo electrónico: ')

                sitio_encontrado = None

                for key, value in sitios.items():
                    if value[0] == sitio_a_buscar:
                        sitio_encontrado = sitios.get(key)

                if sitio_encontrado != None:
                    imprime_sitio(sitio_a_buscar, sitio_encontrado, modo='all')
                else:
                    print("No hay coincidencias con el correo ingresado")
                        
            case _:
                print('Opción inválida')
                time.sleep(1)

'''
FUNCIONES EXCLUSIVAS DEL CIFRADO Y DESCIFRADO
'''
def inicializa_alfabetos():
    clave = quitar_duplicados(CLAVE_ALFABETOS)
    entrada, alfabeto = generar_alfabetos(clave)


def quitar_duplicados(clave):  
    nueva_clave = ''
    for letra in clave:
        if letra not in nueva_clave:
            nueva_clave += letra
    clave = nueva_clave
    return clave


def generar_alfabetos(clave):
    # Definimos cómo se coloca la clave en los
    # alfabetos
    clave1_1 = ''
    clave1_2 = ''
    longitud = len(clave)
    
    if len(clave) % 2 == 0:  # si clave es par 
        for j in range(0,longitud // 2):
            clave1_1 += clave[j]
        for j in range(longitud // 2,longitud):
            clave1_2 += clave[j]
         
    else:  # clave es impar
        limite = (longitud + 1) // 2
        for j in range(0, limite):
            clave1_1 += clave[j]
        for j in range(limite,longitud):
            clave1_2 += clave[j]

    # Generamos el primer alfabeto
    alf1_1 = clave1_1
    alf1_2 = clave1_2
    s_alf = [''] * 2 * NUMERO
   
    for i in ALFABETO:
        if i not in clave and len(alf1_1) <= GIRO:
            alf1_1 +=  i
    for j in ALFABETO:
        if j not in clave and j not in alf1_1:
            alf1_2 +=  j

    s_alf[0], s_alf[1] = alf1_1, alf1_2
    alfabeto[0]= s_alf[0]+ s_alf[1]
    
    # Entradas de los alfabetos
    for k in range(0,NUMERO):
        for i in range(k, len(alfabeto[0]),NUMERO):
            entrada[k] += alfabeto[0][i]

    # Resto de alfabetos       
    for k in range (2, 2 * NUMERO):  
        if k % 2 == 0:
            s_alf[k] = s_alf[0]
                    
        else:
            for i in range(0,len(s_alf[0])):   
                pos = (i + GIRO) % len(s_alf[0])
                s_alf[k] += s_alf[k-2][pos]
                
            alfabeto[(k-1)//2] = s_alf[0] + s_alf[k]
    #mostrar_tabla(entrada,s_alf) #Descomentar en caso de querer guardar la tabla con los alfabetos
    return(entrada,alfabeto)


#función para mostrar la tabla de alfabetos
def mostrar_tabla(entrada, s_alf):
    for i in range(0,NUMERO):
        print(entrada[i], end='')
        if len(entrada[i])-len(entrada[0]) == 0:
            print(' ',s_alf[0].lower())
        else:
            print(' '*2,s_alf[0].lower())

        espacios =len(entrada[0]) + 2
        print(' '*espacios,end='')
        print(s_alf[2*i+1].lower())
    
      
def busqueda(clave): # devuelve el número de alfabeto
    for i in range(0,len(entrada)):
        if clave[0] in entrada[i]:
            return i

        
def cifrarMensaje(clave, mensaje):
    return cifrar_descifrar(clave, mensaje, 'cifrar').upper()


def descifrarMensaje(clave, mensaje):
    return cifrar_descifrar(clave, mensaje, 'descifrar').lower()


def cifrar_descifrar(clave, mensaje,modo):
    clave = ''.join(clave.split())
    palabras = mensaje.split()
    salida = ''
    if modo == 'cifrar' or modo == 'descifrar':
        for i in range(0,len(palabras)):
            n = busqueda(clave[i%len(clave)])
            for j in range(0,len(palabras[i])):
                ind = (n+j)%len(entrada)
                pos = alfabeto[ind].find(palabras[i][j])
                if pos == -1: # No se encuentra el símbolo
                    salida += palabras[i][j]
                else:
                    pos = (pos + len(ALFABETO)//2)%len(ALFABETO)
                    salida += alfabeto[ind][pos]
            salida += ' '
        return salida
'''
FIN FUNCIONES EXCLUSIVAS DEL CIFRADO Y DESCRIFRADO
'''

#Función main
def main():
    while True:
        limpiar_terminal()
        inicializa_alfabetos()
        menu_principal()

        try:        
            opcion_principal = int(input('Opción: '))

            match opcion_principal:
                case 1:
                    control_opcion_1()
                case 2:
                    control_opcion_2()
                case 3:
                    control_opcion_3()
                case 4:
                    control_opcion_4()
                case 5:
                    control_opcion_5()
                case 8:
                    print('Programa finalizado...')
                    break
                case _:
                    print('Opción inválida')
                    time.sleep(1)
        except ValueError:
            print("Por favor introduce un valor válido.")
            time.sleep(1)

#Se invoca funcion main()
if __name__ == '__main__':
    main()
        
                