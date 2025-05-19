from dao.usuario_dao import UsuarioDAO


def main():
    usuarioDAO = UsuarioDAO()

    print(usuarioDAO)

    usuarios = usuarioDAO.obtener_todos()
    print("Todos los usuarios:", usuarioDAO.obtener_todos())

#Se invoca funcion main()
if __name__ == '__main__':
    main()