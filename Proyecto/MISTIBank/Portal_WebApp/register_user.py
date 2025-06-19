import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banksite.settings')
django.setup()

from insurance.models import Usuario

def registrar_usuario():
    username = input("Nombre de usuario: ")
    correo = input("Correo: ")
    password = input("Contraseña: ")

    user = Usuario(username=username, correo=correo)
    user.set_password(password)
    user.save()
    print("Usuario creado correctamente.")

if __name__ == '__main__':
    registrar_usuario()
