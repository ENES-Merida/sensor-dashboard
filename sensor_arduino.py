import time
from datetime import datetime

import serial


class SensorArduinoData:
    def __init__(self):
        # Room termperature range
        self.puerto = "COM3"
        self.baudrate = 9600
        self.temperature = 0.0
        self.humidity = 0.0

    def generate_reading(self):
        ser = serial.Serial(self.puerto, self.baudrate, timeout=1)
        time.sleep(2)  # Espera a que Arduino reinicie
        try:
            linea = ser.readline().decode("utf-8").strip()
            if linea:
                datos = linea.split(",")
                if len(datos) == 4:
                    self.temperature = float(datos[0])
                    self.humidity = float(datos[3])
        except Exception as e:
            print(f"Error: {e}")

        # Modifica los los rangos de Temperatura
        if self.temperature < 25.6:
            status = "normal"
        elif self.temperature < 31.8:
            status = "warning"
        else:
            status = "critical"

        ser.close()
        return {
            "timestamp": datetime.now().isoformat(),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "status": status,
        }
