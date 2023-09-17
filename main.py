import time
import serial
import matplotlib.pyplot as plt
from model import Parking
import matplotlib.animation as animation

# Declaración de las variables a graficar
parkings = [Parking.Parking(1), Parking.Parking(2), Parking.Parking(3)]
records_per_hour = {i: 0 for i in range(60)}

# Selecciona el puerto USB al que está conectado el Arduino y la velocidad del puerto de comunicación en baudios
serialArduino = serial.Serial("COM9", 9600)
time.sleep(1)

fig, (ax, ax_avg, ax_records_per_hour) = plt.subplots(3, 1, figsize=(8, 6))
fig.subplots_adjust(hspace=0.5)

# Gráfica 1: Vehículos por estacionamiento
# Configuración de la gráfica de barras
ax.set_xlabel('Estacionamientos')
ax.set_ylabel('Cantidad de vehículos')
ax.set_title('Uso del estacionamiento en Tiempo Real')
xdata = ['Parking 1', 'Parking 2', 'Parking 3']
ydata = [0, 0, 0]
bars = ax.bar(xdata, ydata)

# Gráfica 2: Gráfica de tiempo promedio en cada estacionamiento
# Configuración de la gráfica de promedios
xdata_avg = ['Parking 1', 'Parking 2', 'Parking 3']
ydata_avg = [0, 0, 0]
avg_line, = ax_avg.plot(xdata_avg, ydata_avg, 'r', marker='o')
ax_avg.set_xlabel('Estacionamiento')
ax_avg.set_ylabel('Promedios')
ax_avg.set_title('Uso promedio por estacionamiento')
ax_avg.set_ylim(0, max(ydata_avg) + 1)

# Gráfica 3: Vehiculos x hora
# Configuración de la gráfica de barras (cantidad de registros por hora)
ax_records_per_hour.set_xlabel('Hora del día')
ax_records_per_hour.set_ylabel('Cantidad de registros')
ax_records_per_hour.set_title('Cantidad de registros por hora del día')


# Función para actualizar la gráfica en cada iteración
def animate(i):
    if serialArduino.inWaiting() > 0:

        #Procesamiento de los datos del Puerto serial conectado al arduino
        data = serialArduino.readline().decode('ascii')
        info = data.split(',')
        parking_index = int(info[0]) - 1
        parkings[parking_index].add_record(Parking.Record(int(info[1])))

        # Gráfica 1: Vehículos por estacionamiento
        # Calcular la cantidad de registros por estacionamiento
        ydata[parking_index] = len(parkings[parking_index].records)
        bars[parking_index].set_height(ydata[parking_index])
        ax.set_ylim(0, max(ydata) + 1)

        # Gráfica 2: Gráfica de tiempo promedio en cada estacionamiento
        # Calcular el promedio de tiempo
        avg_update = parkings[parking_index].avg_time()
        ydata_avg[parking_index] = avg_update
        avg_line.set_ydata(ydata_avg)
        ax_avg.set_ylim(0, max(ydata_avg) + 1)

        # Gráfica 3: Vehiculos x hora
        # Calcular la cantidad de vehiculos por hora en el conjunto de estacionamirntos completo
        hour = parkings[parking_index].records[-1].start_time.minute
        if hour not in records_per_hour:
            records_per_hour[hour] = 1
        else:
            records_per_hour[hour] += 1
        hours = list(records_per_hour.keys())
        quantities = list(records_per_hour.values())
        ax_records_per_hour.bar(hours, quantities)


# Crear una instancia de FuncAnimation para actualizar la gráfica
ani = animation.FuncAnimation(fig, animate, interval=1000)  # Actualiza cada 1 segundo

while True:
    plt.pause(1)  # Pausa el bucle principal durante 1 segundo para permitir que la animación se actualice
