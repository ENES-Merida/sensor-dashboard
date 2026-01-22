import time
from collections import deque
from datetime import datetime

import serial


class SensorArduinoData:
    def __init__(self):
        # Room termperature range
        self.puerto = "/dev/ttyACM0"
        self.baudrate = 9600
        self.temperature = 0.0
        self.temperature1 = 0.0
        self.temperature2 = 0.0
        self.temperature3 = 0.0
        self.humidity = 0.0
        self.status = ""
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
            self.temperature1 = round(32.0 + (time.time() % 10) / 10, 2)
            self.temperature2 = round(33.0 + (time.time() % 10) / 10, 2)
            self.temperature3 = round(34.0 + (time.time() % 10) / 10, 2)
            self.humidity = round(45.0 + (time.time() % 20) / 10, 2)
        else:
            try:
                linea = self.ser.readline().decode("utf-8", errors="ignore").strip()
                print(f"Raw line: {repr(linea)}")
                if linea:
                    print("entra aqui")
                    datos = linea.split(",")
                    print(datos)
                    if len(datos) == 4:
                        self.temperature1 = float(datos[0])
                        self.temperature2 = float(datos[1])
                        self.temperature3 = float(datos[2])
                        self.humidity = float(datos[3])
            except ValueError as e:
                print(f"❌ Error parseando números: {e}")
            except Exception as e:
                print(f"❌ Error leyendo serial: {e}")
                self.ser = None

        # Modifica los los rangos de Temperatura
        self.temperature = (
            self.temperature1 + self.temperature2 + self.temperature3
        ) / 3
        if self.temperature < 25.6:
            self.status = "normal"
        elif self.temperature < 31.1:
            self.status = "warning"
        else:
            self.status = "critical"

        # ser.close()
        return {
            "timestamp": datetime.now().isoformat(),
            "temperature1": self.temperature1,
            "temperature2": self.temperature2,
            "temperature3": self.temperature3,
            "humidity": self.humidity,
            "status": self.status,
        }

    def close(self):
        """Cierra la conexión serial"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 Conexión serial cerrada")


# Mantiene las últimas 50 lecturas en memoria
sensor_history = deque(maxlen=20)
