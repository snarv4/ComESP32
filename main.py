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
    def __init__(self, valor)
        self.valor = valor

# --- Logica de RED
sock = socket(socket.AF_INET. socket.SOCK_STREAM)