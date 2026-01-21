import serial
import matplotlib.pyplot as plt
import time

# ===============================
# CONFIGURACIÓN DEL PUERTO SERIE
# ===============================
puerto = 'COM3'        # Cambia según tu sistema
baudrate = 9600

ser = serial.Serial(puerto, baudrate, timeout=1)
time.sleep(2)  # Espera a que Arduino reinicie

# ===============================
# LISTAS PARA DATOS
# ===============================
tiempo = []
temp1 = []
temp2 = []
temp3 = []
humedad = []

t0 = time.time()

# ===============================
# CONFIGURACIÓN DE LA FIGURA
# ===============================
plt.ion()

fig, axs = plt.subplots(4, 1, sharex=True, figsize=(8, 10))

# ===============================
# BUCLE PRINCIPAL
# ===============================
while True:
    try:
        linea = ser.readline().decode('utf-8').strip()

        if linea:
            datos = linea.split(',')

            if len(datos) == 4:
                t = time.time() - t0

                tiempo.append(t)
                temp1.append(float(datos[0]))
                temp2.append(float(datos[1]))
                temp3.append(float(datos[2]))
                humedad.append(float(datos[3]))

                # -------- SUBPLOT 1 --------
                axs[0].clear()
                axs[0].plot(tiempo, temp1)
                axs[0].set_ylabel('Temp 1 (°C)')
                axs[0].grid(True)

                # -------- SUBPLOT 2 --------
                axs[1].clear()
                axs[1].plot(tiempo, temp2)
                axs[1].set_ylabel('Temp 2 (°C)')
                axs[1].grid(True)

                # -------- SUBPLOT 3 --------
                axs[2].clear()
                axs[2].plot(tiempo, temp3)
                axs[2].set_ylabel('Temp 3 (°C)')
                axs[2].grid(True)

                # -------- SUBPLOT 4 --------
                axs[3].clear()
                axs[3].plot(tiempo, humedad)
                axs[3].set_ylabel('Humedad (%)')
                axs[3].set_xlabel('Tiempo (s)')
                axs[3].grid(True)

                fig.suptitle('Temperatura y Humedad en Tiempo Real', fontsize=14)
                plt.pause(0.1)

    except KeyboardInterrupt:
        print("Programa detenido por el usuario")
        break

    except Exception as e:
        print("Error:", e)

ser.close()
