
from modelo.usuario import Usuario

import mysql
from mysql.connector import (connection)
from mysql.connector import errorcode

class UsuarioDAO:
    def __init__(self):
        print("init")

    def conectar(self):
        try:
            cnx = connection.MySQLConnection(user='development',
                password='development',
                host='localhost',
                database='banco_banpatito')
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Algo está mal con tu usuario y contraseña. El acceso fue denegado.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La Base de Datos no existe.")
            else:
                print(err)

        return cnx

    def insertar(self, sitio, username, password, secretkey, email):
        exito = False
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("INSERT INTO `user_sites_storage`.`usuario` (`sitio`, `username`, `password`, `secretkey`, `email`) VALUES (?,?,?,?,?)", (sitio, username, password, secretkey, email))
            conexion.commit()
            print(cursor.rowcount, " registros insertados.")
            print("El identificador registrado fue el: ", cursor.lastrowid)

            exito = True
        except mysql.connector.Error as e:
            print("Error code:", e.errno)        # error number
            print("SQLSTATE value:", e.sqlstate) # SQLSTATE value
            print("Error message:", e.msg)       # error message
            print("Error:", e)                   # errno, sqlstate, msg values
            s = str(e)
            print("Error:", s)
        
        finally:
            cursor.close()
            conexion.close()

        return exito


    def obtener_por_id(self, id_usuario):
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            
            cursor.execute("SELECT * FROM usuario WHERE id=?", (id_usuario))
            usuario = cursor.fetchone()

            if usuario:
                return Usuario()
            return None
        except mysql.connector.Error as e:
            print("Error code:", e.errno)        # error number
            print("SQLSTATE value:", e.sqlstate) # SQLSTATE value
            print("Error message:", e.msg)       # error message
            print("Error:", e)                   # errno, sqlstate, msg values
            s = str(e)
            print("Error:", s)
        
        finally:
            cursor.close()
            conexion.close()


        

    def obtener_todos(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM banco_banpatito.cliente")
        usuarios = cursor.fetchall()
        conexion.close()
        return [{"idusuario": u[0], "idcliente": u[1], "username": u[2], "password": u[3], "email": u[4], "fecha_creacion": u[5], "fecha_actualizacion": u[6]} for u in usuarios]


    def actualizar(self, id_usuario, nombre=None, email=None):
        conexion = self.conectar()
        cursor = conexion.cursor()
        actualizaciones = []
        parametros = []
        if nombre:
            actualizaciones.append("nombre=?")
            parametros.append(nombre)
        if email:
            actualizaciones.append("email=?")
            parametros.append(email)

        if not actualizaciones:
            conexion.close()
            return 0

        parametros.append(id_usuario)
        query = f"UPDATE usuarios SET {', '.join(actualizaciones)} WHERE id=?"
        cursor.execute(query, tuple(parametros))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas

    def eliminar(self, id_usuario):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas

