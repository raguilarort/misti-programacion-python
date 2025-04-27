from Modelo.Nodos.NodoDoble import NodoDoble

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, v):
        if self.raiz is None:
            self.raiz = NodoDoble(v)
        else:
            self.insertar_recursivo(self.raiz, v)

    def insertar_recursivo(self, nodo_actual, v):
        if v < nodo_actual.value:
            if nodo_actual.left is None:
                nodo_actual.left = NodoDoble(v)
            else:
                self.insertar_recursivo(nodo_actual.left, v)
        elif v > nodo_actual.value:
            if nodo_actual.right is None:
                nodo_actual.right = NodoDoble(v)
            else:
                self.insertar_recursivo(nodo_actual.right, v)
        else:
            print("El dato ya existe en el árbol.")

    def buscar(self, dato):
        return self.buscar_recursivo(self.raiz, dato)

    def buscar_recursivo(self, nodo_actual, dato):
        if nodo_actual is None:
            return False
        if nodo_actual.value == dato:
            return True
        if dato < nodo_actual.value:
            return self.buscar_recursivo(nodo_actual.left, dato)
        return self.buscar_recursivo(nodo_actual.right, dato)
    
    def eliminar(self, dato):
        self.raiz = self.eliminar_recursivo(self.raiz, dato)

    def eliminar_recursivo(self, nodo_actual, dato):
        if nodo_actual is None:
            return nodo_actual

        if dato < nodo_actual.dato:
            nodo_actual.left = self.eliminar_recursivo(nodo_actual.left, dato)
        elif dato > nodo_actual.dato:
            nodo_actual.right = self.eliminar_recursivo(nodo_actual.right, dato)
        else:
            if nodo_actual.left is None:
                return nodo_actual.right
            elif nodo_actual.right is None:
                return nodo_actual.left

            nodo_actual.value = self.min_valor(nodo_actual.right)
            nodo_actual.right = self.eliminar_recursivo(nodo_actual.right, nodo_actual.value)
        return nodo_actual
    
    def min_valor(self, nodo):
        while nodo.left is not None:
            nodo = nodo.left
        return nodo.value

    def mostrar_contenido(self):
        self.generar_html_estetico1()
        self.generar_html_estetico2()
    
    
    def generar_html_estetico1(self, nombre_archivo="arbol.html"):
        def generar_nodo_html(nodo):
            if not nodo:
                return ""
            return f"""
                <div class="nodo">
                    <div class="valor">{nodo.value}</div>
                    <div class="hijos">
                        <div class="izquierda">{generar_nodo_html(nodo.left)}</div>
                        <div class="derecha">{generar_nodo_html(nodo.right)}</div>
                    </div>
                </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Árbol Binario</title>
            <style>
                .nodo {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    border: 1px solid #ccc;
                    padding: 10px;
                    margin: 5px;
                }}
                .valor {{
                    font-weight: bold;
                }}
                .hijos {{
                    display: flex;
                }}
                .izquierda, .derecha {{
                    padding: 10px;
                }}
            </style>
        </head>
        <body>
            <h1>Árbol Binario</h1>
            <div class="arbol">
                {generar_nodo_html(self.raiz)}
            </div>
        </body>
        </html>
        """

        with open(nombre_archivo, "w") as archivo:
            archivo.write(html)

        print(f"Se ha generado el archivo HTML: {nombre_archivo}")

    def generar_html_estetico2(self, nombre_archivo="arbol2.html"):
        def generar_nodo_html(nodo):
            if not nodo:
                return ""
            return f"""
                <ul>
                    <li>
                        <a href="#">{nodo.value}</a>
                        <ul>
                            <li>
                                {generar_nodo_html(nodo.left)}
                            </li>
                            <li>
                                {generar_nodo_html(nodo.right)}
                            </li>
                        </ul>
                    </li>
                </ul>
            """

        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>&Aacute;rbol Binario</title>
            <link rel="stylesheet" href="estilos_arbol.css">
        </head>
        <body>
            <h1>&Aacute;rbol Binario</h1>
            <div class="arbol-binario">
                <div class="tree">
                    {generar_nodo_html(self.raiz)}
                </div>
            </div>
        </body>
        </html>
        """

        with open(nombre_archivo, "w") as archivo:
            archivo.write(html)

        print(f"Se ha generado el archivo HTML: {nombre_archivo}")


# Ejemplo de uso
#if __name__ == "__main__":
#    arbol_altura = ArbolBinario()
#    arbol_altura.insertar(50)
#    arbol_altura.insertar(30)
#    arbol_altura.insertar(70)
#    arbol_altura.insertar(20)
#    arbol_altura.insertar(40)
#    arbol_altura.insertar(60)
#    arbol_altura.insertar(80)
#    arbol_altura.insertar(10)
#    arbol_altura.insertar(35)
#    arbol_altura.insertar(75)
#
#    
#    print("\nRepresentación gráfica del árbol con altura:")
#    arbol_altura.imprimir_grafico_con_altura()