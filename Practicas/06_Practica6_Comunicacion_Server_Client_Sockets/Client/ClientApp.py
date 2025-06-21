import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import socket
import threading
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

HOST = '127.0.0.1'  # La IP del servidor
PORT = 65432        # El puerto del servidor

class ClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Cliente de Datos y Gráficas")
        master.geometry("700x550")

        # Frame de Conexión
        connect_frame = tk.LabelFrame(master, text="Conexión al Servidor")
        connect_frame.pack(padx=10, pady=10, fill="x")

        self.server_ip_label = tk.Label(connect_frame, text="IP Servidor:")
        self.server_ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.server_ip_entry = tk.Entry(connect_frame, width=15)
        self.server_ip_entry.insert(0, HOST)
        self.server_ip_entry.grid(row=0, column=1, padx=5, pady=5)

        self.server_port_label = tk.Label(connect_frame, text="Puerto:")
        self.server_port_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.server_port_entry = tk.Entry(connect_frame, width=7)
        self.server_port_entry.insert(0, str(PORT))
        self.server_port_entry.grid(row=0, column=3, padx=5, pady=5)

        self.connect_button = tk.Button(connect_frame, text="Conectar", command=self.connect_to_server)
        self.connect_button.grid(row=0, column=4, padx=10, pady=5)

        self.disconnect_button = tk.Button(connect_frame, text="Desconectar", command=self.disconnect_from_server, state=tk.DISABLED)
        self.disconnect_button.grid(row=0, column=5, padx=5, pady=5)
        
        self.status_label = tk.Label(connect_frame, text="Estado: Desconectado", fg="red")
        self.status_label.grid(row=1, column=0, columnspan=6, pady=5)

        # Frame de Datos
        data_frame = tk.LabelFrame(master, text="Datos Recibidos del Servidor")
        data_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.data_text_area = scrolledtext.ScrolledText(data_frame, width=80, height=10, state=tk.DISABLED)
        self.data_text_area.pack(padx=5, pady=5, fill="both", expand=True)

        self.get_data_button = tk.Button(data_frame, text="Solicitar Datos", command=self.request_data, state=tk.DISABLED)
        self.get_data_button.pack(pady=5)

        # Frame de Gráficas
        plot_frame = tk.LabelFrame(master, text="Visualización de Gráficas")
        plot_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 3.5)) # Ajusta el tamaño según necesidad
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ax.set_title("Gráfica de Datos")
        self.ax.set_xlabel("Muestras")
        self.ax.set_ylabel("Valores")
        self.canvas.draw()

        self.plot_button = tk.Button(plot_frame, text="Graficar Temperaturas", command=lambda: self.plot_data("temperaturas"), state=tk.DISABLED)
        self.plot_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.plot_hum_button = tk.Button(plot_frame, text="Graficar Humedad", command=lambda: self.plot_data("humedad"), state=tk.DISABLED)
        self.plot_hum_button.pack(side=tk.LEFT, padx=5, pady=5)


        self.client_socket = None
        self.connected = False
        self.received_data = {} # Para almacenar los datos parseados

    def update_status(self, message, color):
        self.status_label.config(text=f"Estado: {message}", fg=color)

    def log_to_data_area(self, message):
        self.data_text_area.config(state=tk.NORMAL)
        self.data_text_area.insert(tk.END, message + "\n")
        self.data_text_area.see(tk.END)
        self.data_text_area.config(state=tk.DISABLED)

    def connect_to_server(self):
        if self.connected:
            messagebox.showwarning("Advertencia", "Ya estás conectado al servidor.")
            return

        host = self.server_ip_entry.get()
        port_str = self.server_port_entry.get()

        if not host or not port_str:
            messagebox.showerror("Error", "La IP y el Puerto del servidor son requeridos.")
            return
        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(5) # Timeout para la conexión
            self.client_socket.connect((host, port))
            self.connected = True
            self.update_status(f"Conectado a {host}:{port}", "green")
            self.log_to_data_area(f"Conectado al servidor {host}:{port}.")
            
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.get_data_button.config(state=tk.NORMAL)
            self.server_ip_entry.config(state=tk.DISABLED)
            self.server_port_entry.config(state=tk.DISABLED)

        except socket.timeout:
            messagebox.showerror("Error de Conexión", f"Tiempo de espera agotado al conectar con {host}:{port}.")
            self.cleanup_connection()
        except ConnectionRefusedError:
            messagebox.showerror("Error de Conexión", f"Conexión rechazada por el servidor en {host}:{port}.")
            self.cleanup_connection()
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor: {e}")
            self.cleanup_connection()

    def disconnect_from_server(self):
        if self.connected and self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR) # Notifica al servidor
                self.client_socket.close()
            except Exception as e:
                self.log_to_data_area(f"Error durante la desconexión: {e}")
        
        self.cleanup_connection()
        self.log_to_data_area("Desconectado del servidor.")
        self.update_status("Desconectado", "red")


    def cleanup_connection(self):
        self.client_socket = None
        self.connected = False
        self.received_data = {}
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.get_data_button.config(state=tk.DISABLED)
        self.plot_button.config(state=tk.DISABLED)
        self.plot_hum_button.config(state=tk.DISABLED)
        self.server_ip_entry.config(state=tk.NORMAL)
        self.server_port_entry.config(state=tk.NORMAL)
        self.ax.clear() # Limpia la gráfica anterior
        self.ax.set_title("Gráfica de Datos")
        self.ax.set_xlabel("Muestras")
        self.ax.set_ylabel("Valores")
        self.canvas.draw()


    def request_data(self):
        if not self.connected or not self.client_socket:
            messagebox.showerror("Error", "No estás conectado al servidor.")
            return

        try:
            self.log_to_data_area("Solicitando datos al servidor ('get_data')...")
            self.client_socket.sendall(b"get_data")
            
            response_bytes = self.client_socket.recv(4096)
            if not response_bytes:
                self.log_to_data_area("El servidor cerró la conexión o no envió datos.")
                self.disconnect_from_server()
                return

            response_str = response_bytes.decode('utf-8')
            self.log_to_data_area(f"Respuesta recibida (raw): {response_str[:200]}...") # Muestra solo una parte

            try:
                self.received_data = json.loads(response_str)
                self.log_to_data_area("Datos JSON parseados correctamente:")
                self.log_to_data_area(json.dumps(self.received_data, indent=2))
                
                # Habilitar botones de graficación
                if "temperaturas" in self.received_data and isinstance(self.received_data["temperaturas"], list):
                    self.plot_button.config(state=tk.NORMAL)
                else:
                    self.plot_button.config(state=tk.DISABLED)
                
                if "humedad" in self.received_data and isinstance(self.received_data["humedad"], list):
                    self.plot_hum_button.config(state=tk.NORMAL)
                else:
                    self.plot_hum_button.config(state=tk.DISABLED)

            except json.JSONDecodeError:
                self.log_to_data_area("Error: La respuesta del servidor no es un JSON válido.")
                self.received_data = {}
                self.plot_button.config(state=tk.DISABLED)
                self.plot_hum_button.config(state=tk.DISABLED)


        except socket.timeout:
            self.log_to_data_area("Error: Tiempo de espera agotado esperando respuesta del servidor.")
            messagebox.showerror("Error de Red", "Tiempo de espera agotado.")
        except ConnectionResetError:
            self.log_to_data_area("Error: La conexión fue reiniciada por el servidor.")
            messagebox.showerror("Error de Red", "Conexión reiniciada por el servidor.")
            self.disconnect_from_server()
        except BrokenPipeError:
            self.log_to_data_area("Error: Tubería rota. Posiblemente el servidor cerró la conexión abruptamente.")
            messagebox.showerror("Error de Red", "La conexión con el servidor se interrumpió.")
            self.disconnect_from_server()
        except Exception as e:
            self.log_to_data_area(f"Error solicitando datos: {e}")
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
            # self.disconnect_from_server()

    def plot_data(self, data_key):
        if not self.received_data:
            messagebox.showinfo("Información", "No hay datos para graficar. Solicita datos primero.")
            return

        if data_key not in self.received_data or not isinstance(self.received_data[data_key], list):
            messagebox.showerror("Error de Datos", f"No se encontró la clave '{data_key}' o no es una lista en los datos recibidos.")
            return
        
        data_to_plot = self.received_data[data_key]
        description = self.received_data.get("descripcion_datos", "Datos")

        self.ax.clear() # Limpiar gráfica anterior
        self.ax.plot(data_to_plot, marker='o', linestyle='-')
        self.ax.set_title(f"Gráfica de {data_key.capitalize()}")
        self.ax.set_xlabel("Índice de Muestra")
        self.ax.set_ylabel(f"Valor de {data_key.capitalize()}")
        self.ax.grid(True)
        self.canvas.draw()
        self.log_to_data_area(f"Graficando datos de '{data_key}'.")


def main():
    root = tk.Tk()
    app = ClientApp(root)
    
    def on_closing():
        app.disconnect_from_server() 
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()