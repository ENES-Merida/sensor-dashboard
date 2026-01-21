from collections import deque
from datetime import datetime

import requests


class SensorData:
    def __init__(self):
        # Room termperature range
        self.api_url = "https://api.open-meteo.com/v1/forecast"

    def generate_reading(self):
        params = {
            "latitude": 20.9754,
            "longitude": -89.617,
            "current": ["temperature_2m", "relative_humidity_2m"],
            "timezone": "auto",
        }
        response = requests.get(self.api_url, params=params)
        response.raise_for_status()

        data = response.json()
        temperature = data["current"]["temperature_2m"]
        humidity = data["current"]["relative_humidity_2m"]

        # Modifica los los rangos de Temperatura
        if temperature < 21.6:
            status = "normal"
        elif temperature < 27.3:
            status = "warning"
        else:
            status = "critical"

        return {
            "timestamp": datetime.now().isoformat(),
            "temperature": temperature,
            "humidity": humidity,
            "status": status,
        }


# Store the last 20 recent readings for charts
recent_readings = deque(maxlen=20)
