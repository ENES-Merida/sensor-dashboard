import time
from datetime import datetime
from collections import deque

import serial


class SensorArduinoData:
    def __init__(self):
        # Room termperature range
        self.puerto = "/dev/ttyACM0"
        self.baudrate = 9600
        self.temperature = 0.0
        self.humidity = 0.0
        self.ser = None
        self._connect()

    def _connect(self):
        """Establece conexión persistente con Arduino"""
        try:
            self.ser = serial.Serial(self.puerto, self.baudrate, timeout=2)
            time.sleep(2)  # Espera a que Arduino reinicie
            print(f"✅ Conectado a Arduino en {self.puerto}")
        except Exception as e:
            print(f"❌ Error conectando a Arduino: {e}")
            self.ser = None

    def generate_reading(self):
        if self.ser is None or not self.ser.is_open:
            self._connect()
        if self.ser is None:
            print("⚠️  No hay conexión con Arduino, usando datos de prueba")
            # Datos de prueba si no hay Arduino conectado
            self.temperature = 22.0 + (time.time() % 10) / 10
            self.humidity = 45.0 + (time.time() % 20) / 10
        else:
            try:
                linea = self.ser.readline().decode("utf-8", errors="ignore").strip()
                print(f"Raw line: {repr(linea)}")
                if linea:
                    print("entra aqui")
                    datos = linea.split(",")
                    print(datos)
                    if len(datos) == 4:
                        self.temperature = float(datos[0])
                        self.humidity = float(datos[3])
            except ValueError as e:
                print(f"❌ Error parseando números: {e}")
            except Exception as e:
                print(f"❌ Error leyendo serial: {e}")
                self.ser = None

        # Modifica los los rangos de Temperatura
        if self.temperature < 25.6:
            status = "normal"
        elif self.temperature < 31.8:
            status = "warning"
        else:
            status = "critical"

        # ser.close()
        return {
            "timestamp": datetime.now().isoformat(),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "status": status,
        }

    def close(self):
        """Cierra la conexión serial"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 Conexión serial cerrada")

# Mantiene las últimas 50 lecturas en memoria
sensor_history = deque(maxlen=20)