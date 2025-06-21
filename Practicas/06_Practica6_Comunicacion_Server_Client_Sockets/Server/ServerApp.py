import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
import json

# Simulación de base de datos
DATABASE = {
    "temperaturas": [20, 21, 22, 20, 23, 24, 25, 22, 21, 20, 26, 27],
    "humedad": [60, 62, 61, 63, 60, 59, 58, 60, 61, 63, 64, 62],
    "descripcion_datos": "Datos de ejemplo: temperaturas (°C) y humedad (%) mensuales."
}

HOST = '127.0.0.1'  # Dirección IP local (localhost)
PORT = 65432        # Puerto para escuchar (no privilegiado)

class ServerApp:
    def __init__(self, master):
        self.master = master
        master.title("Servidor de Datos")
        master.geometry("500x400")

        self.log_label = tk.Label(master, text="Registro del Servidor:")
        self.log_label.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(master, width=60, height=15, state=tk.DISABLED)
        self.log_area.pack(padx=10, pady=5)

        self.start_button = tk.Button(master, text="Iniciar Servidor", command=self.start_server_thread)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Detener Servidor", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.server_socket = None
        self.running = False
        self.client_threads = []

    def log_message(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def start_server_thread(self):
        if not self.running:
            self.server_thread = threading.Thread(target=self.run_server, daemon=True)
            self.server_thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.log_message("Servidor iniciando...")
        else:
            messagebox.showwarning("Advertencia", "El servidor ya está en ejecución.")


    def run_server(self):
        self.running = True
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()
            self.log_message(f"Servidor escuchando en {HOST}:{PORT}")

            while self.running:
                try:
                    self.server_socket.settimeout(1.0) # Timeout para permitir la detención
                    conn, addr = self.server_socket.accept()
                    self.log_message(f"Conexión aceptada de {addr}")
                    client_handler = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                    client_handler.start()
                    self.client_threads.append(client_handler)
                except socket.timeout:
                    continue 
                except OSError as e:
                    if self.running:
                        self.log_message(f"Error de socket al aceptar conexiones: {e}")
                    break 

        except Exception as e:
            if self.running :
                 self.log_message(f"Error al iniciar el servidor: {e}")
        finally:
            self.cleanup_server()

    def handle_client(self, conn, addr):
        try:
            with conn:
                while self.running:
                    data = conn.recv(1024)
                    if not data:
                        self.log_message(f"Cliente {addr} desconectado.")
                        break
                    
                    request = data.decode('utf-8')
                    self.log_message(f"Cliente {addr} solicitó: {request}")

                    if request == "get_data":
                        response = json.dumps(DATABASE).encode('utf-8')
                        conn.sendall(response)
                        self.log_message(f"Datos enviados a {addr}")
                    elif request == "ping":
                        conn.sendall(b"pong")
                    else:
                        conn.sendall(b"Comando no reconocido")
        except ConnectionResetError:
            self.log_message(f"Conexión con {addr} reiniciada por el cliente.")
        except Exception as e:
            if self.running:
                self.log_message(f"Error manejando cliente {addr}: {e}")
        finally:
            if conn:
                conn.close()


    def stop_server(self):
        if self.running:
            self.running = False
            self.log_message("Deteniendo el servidor...")

            if hasattr(self, 'server_thread') and self.server_thread.is_alive():
                self.server_thread.join(timeout=2.0)

            if self.server_socket:
                try:
                    self.server_socket.close() 
                except Exception as e:
                    self.log_message(f"Error al cerrar el socket del servidor: {e}")
                self.server_socket = None

            for thread in self.client_threads:
                if thread.is_alive():
                    thread.join(timeout=1.0) 
            self.client_threads = []

            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.log_message("Servidor detenido.")
        else:
            messagebox.showwarning("Advertencia", "El servidor no está en ejecución.")
    
    def cleanup_server(self):
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception as e:
                self.log_message(f"Error en cleanup cerrando socket del servidor: {e}")
        self.server_socket = None
        self.running = False
        self.master.after(0, self.update_gui_on_stop)


    def update_gui_on_stop(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if not self.running: # Para evitar mensajes duplicados si stop_server ya lo hizo
            if not any("Servidor detenido." in self.log_area.get("1.0", tk.END).splitlines()[-2:]):
                 self.log_message("Servidor detenido o falló al iniciar.")


def main():
    root = tk.Tk()
    app = ServerApp(root)
    
    def on_closing():
        app.stop_server()
        root.after(100, root.destroy)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()