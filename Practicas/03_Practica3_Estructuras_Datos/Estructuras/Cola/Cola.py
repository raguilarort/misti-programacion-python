class Cola:
    def __init__(self):
        self.elementos = []

    def esta_vacia(self):
        return len(self.elementos) == 0

    def encolar(self, elemento):
        self.elementos.append(elemento)

    def desencolar(self):
        if not self.esta_vacia():
            return self.elementos.pop(0)
        else:
            return "La cola está vacía"

    def tamano(self):
        return len(self.elementos)
    
    def mostrar(self):#método que es para imprimir
        print("Contenido de la cola:", self.elementos)