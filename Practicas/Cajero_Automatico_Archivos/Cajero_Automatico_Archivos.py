import os
import pandas as pd
from fpdf import FPDF
from PIL import Image
from IPython.display import display, Image as IPImage

CLIENTES_FILE = "clientes.xlsx"
MOVIMIENTOS_FILE = "movimientos.xlsx"
IMG_DIR = "imagenes"

def inicializar_archivos():
    if not os.path.exists(CLIENTES_FILE):
        df = pd.DataFrame(columns=["RFC", "Nombre", "Usuario", "Password", "Saldo"])
        df.to_excel(CLIENTES_FILE, index=False)

    if not os.path.exists(MOVIMIENTOS_FILE):
        df = pd.DataFrame(columns=["RFC", "Movimiento", "Monto", "Nuevo Saldo"])
        df.to_excel(MOVIMIENTOS_FILE, index=False)

    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)

def registrar_cliente():
    rfc = input("RFC: ")
    nombre = input("Nombre completo: ")
    usuario = input("Usuario: ")
    password = input("Password: ")
    saldo = float(input("Saldo inicial: "))

    df = pd.read_excel(CLIENTES_FILE)
    if rfc in df["RFC"].values:
        print("Ese RFC ya está registrado.")
        return

    df.loc[len(df.index)] = [rfc, nombre, usuario, password, saldo]
    df.to_excel(CLIENTES_FILE, index=False)
    print("✔ Cliente registrado correctamente.")

def iniciar_sesion():
    rfc = input("RFC: ")
    usuario = input("Usuario: ")
    password = input("Password: ")

    df = pd.read_excel(CLIENTES_FILE)
    cliente = df[(df["RFC"] == rfc) & (df["Usuario"] == usuario) & (df["Password"] == password)]

    if not cliente.empty:
        return cliente.iloc[0]
    else:
        print(" Credenciales incorrectas.")
        return None

def registrar_movimiento(rfc, movimiento, monto, nuevo_saldo):
    df = pd.read_excel(MOVIMIENTOS_FILE)
    df.loc[len(df.index)] = [rfc, movimiento, monto, nuevo_saldo]
    df.to_excel(MOVIMIENTOS_FILE, index=False)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Recibo de {movimiento}", ln=True)
    pdf.cell(200, 10, txt=f"RFC: {rfc}", ln=True)
    pdf.cell(200, 10, txt=f"Monto: ${monto}", ln=True)
    pdf.cell(200, 10, txt=f"Nuevo saldo: ${nuevo_saldo}", ln=True)
    pdf.output(f"recibo_{rfc}_{movimiento}.pdf")

def menu_cliente(cliente):
    while True:
        print("\n1. Consultar saldo")
        print("2. Retirar")
        print("3. Depositar")
        print("4. Ver recibos PDF generados")
        print("0. Salir")
        opcion = input("Selecciona una opción: ")

        df = pd.read_excel(CLIENTES_FILE)
        idx = df[df["RFC"] == cliente["RFC"]].index[0]
        saldo_actual = df.at[idx, "Saldo"]

        if opcion == "1":
            print(f" Tu saldo actual es: ${saldo_actual}")

        elif opcion == "2":
            monto = float(input("Monto a retirar: "))
            if monto <= saldo_actual:
                df.at[idx, "Saldo"] -= monto
                df.to_excel(CLIENTES_FILE, index=False)
                registrar_movimiento(cliente["RFC"], "Retiro", monto, df.at[idx, "Saldo"])
                print(" Retiro realizado correctamente.")
            else:
                print(" Fondos insuficientes.")

        elif opcion == "3":
            monto = float(input("Monto a depositar: "))
            df.at[idx, "Saldo"] += monto
            df.to_excel(CLIENTES_FILE, index=False)
            registrar_movimiento(cliente["RFC"], "Depósito", monto, df.at[idx, "Saldo"])
            print("✔ Depósito realizado correctamente.")

        elif opcion == "4":
            print(" Archivos PDF generados:")
            for archivo in os.listdir():
                if archivo.endswith(".pdf") and cliente["RFC"] in archivo:
                    print("📄", archivo)

        elif opcion == "0":
            print(" Sesión cerrada.")
            break
        else:
            print(" Opción inválida.")

def main():
    inicializar_archivos()
    while True:
        print("\n=== CAJERO AUTOMÁTICO EN JUPYTER ===")
        print("1. Iniciar sesión")
        print("2. Registrar nuevo cliente")
        print("0. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            cliente = iniciar_sesion()
            if cliente is not None:
                menu_cliente(cliente)
        elif opcion == "2":
            registrar_cliente()
        elif opcion == "0":
            print(" ¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

main()
