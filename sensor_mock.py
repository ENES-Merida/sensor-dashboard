from collections import deque
import random
from datetime import datetime

class SensorData:
    def __init__(self):
        # Room termperature range
        self.min_temp = 18.0
        self.max_temp = 36.0
        self.min_humidity = 30.0
        self.max_humidity = 65.0

    def generate_reading(self):
        temperature = round(random.uniform(self.min_temp, self.max_temp), 1)
        humidity = round(random.uniform(self.min_humidity, self.max_humidity), 1)

        # Modifica los los rangos de Temperatura
        if temperature < 25.6:
            status = "normal"
        elif temperature < 31.8:
            status = "warning"
        else:
            status = "critical"

        return {
            "timestamp": datetime.now().isoformat(),
            "temperature": temperature,
            "humidity": humidity,
            "status": status
        }

# Store the last 20 recent readings for charts
recent_readings = deque(maxlen=20)
