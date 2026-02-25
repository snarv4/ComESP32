import tkinter as tk 
from tkinter import ttk 
import socket
import threading
import time

#---CONFIGURACION---
IP_ESP32 = "192.168.20.57"
PUERTO = 80

#--- CLASE DE DATOS (Para Practicar)
class DatosSensor:
    def __init__(self, valor):
        self.valor = valor

# --- Logica de RED
sock = socket(socket.AF_INET. socket.SOCK_STREAM)

def conectar():
    try:
        sock.connect((IP_ESP32, PUERTO))
        print("Conectado al ESP32")
        threading.Thread(target=recibir_datos, daemon=True).start()
    except:
        print("Error al conectar")
def recibir_datos():
    while True:
        try:
            data = sock.recv(1024).decode().strip()
            if data:
                #Instanciamos la clase para procesar el valor
                sensor = DatosSensor(int(data))
                #Actualizar la barra en la interfaz
                progress['value'] = sensor.valor
                lbl_valor.config(text=f"Potenciometro: {sensor.valor}")
        except:
            break

def led_on(): sock.send(b'ON')
def led_off(): sock.send(b'OFF')

# --- INTERFAZ GRAFICA ---
root = tk.Tk()
root.title("Control ESP32")

#Diseño con GRID
tk.Label(root)