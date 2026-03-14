import network
import socket
import time
from machine import Pin, ADC

# --- CONFIGURACIÓN DE RED ---
SSID = "RedWifi"
PASSWORD = "Password"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("Conectado! IP:", wlan.ifconfig()[0])

conectar_wifi()

# --- HARDWARE ---
led = Pin(12, Pin.OUT) 
pot = ADC(Pin(32))
pot.atten(ADC.ATTN_11DB) 

# --- SOCKET (Servidor de Control) ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SO_REUSEADDR ayuda a que el ESP32 no bloquee el puerto si lo reinicias rápido
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 80)) #puerto 80 para HTTP, aunque no estamos sirviendo páginas, es común para control simple
server.listen(1)

print("Esperando conexión de la PC...")

while True:
    conn, addr = server.accept()
    print("PC conectada desde:", addr)
    
    # Timeout corto en lugar de setblocking(False)
    conn.settimeout(0.05) 
    
    while True:
        try:
            # 1. Leer potenciómetro y enviar a la PC
            val_pot = pot.read()
            conn.send(str(val_pot).encode() + b'\n')
            
            # 2. Revisar si la PC mandó una orden para el LED
            try:
                data = conn.recv(1024)
                # Usamos la palabra clave 'in' para buscar el comando dentro de los bytes
                if b'ON' in data: 
                    led.value(1)
                if b'OFF' in data: 
                    led.value(0)
            except OSError:
                # Si ocurre un OSError aquí, simplemente significa que pasaron 
                # los 0.05s y no llegó ningún comando. Es normal, lo ignoramos.
                pass 
                
            time.sleep(0.1) # Pequeño respiro para no saturar el router
            
        except Exception as e:
            # Si el error llega a este bloque, es porque la PC cerró el programa
            print("Conexión finalizada:", e)
            conn.close()
            break