import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banksite.settings')
django.setup()

from insurance.models import Usuario
#registrar un nuevo usuario desde la consola
def registrar_usuario():
    username = input("Nombre de usuario: ")
    correo = input("Correo: ")
    password = input("Contraseña: ")

    user = Usuario(username=username, correo=correo)
    user.set_password(password)#se aplica hash seguro a la contraseña usando el algoritmo PBKDF2
    #usa un salt único para cada usuario, lo que impide ataques por diccionario o rainbow table
    user.save()
    print("Usuario creado correctamente.")

if __name__ == '__main__':
    registrar_usuario()

#Django utiliza el algoritmo PBKDF2 para proteger contraseñas. Este algoritmo aplica miles de iteraciones de hash
#combinadas con un "salt" único por usuario, lo que hace que incluso contraseñas iguales generen hashes distintos. 
#y esto mismo evita ataques con rainbow tables (tablas precalculadas de hashes), y las múltiples iteraciones hacen que los 
#intentos de fuerza bruta sean computacionalmente costosos. Gracias a esto, las contraseñas nunca se almacenan en texto plano 
#ni pueden ser revertidas a su forma original.
