import matplotlib.pyplot as plt
import numpy as np
import threading
from matplotlib.animation import FuncAnimation

# Inicializar figura para graficar
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_xlabel("XA")
ax.set_ylabel("YA")

# Inicializar la trayectoria
trayectoria = []

# Funcion para generar los nuevos puntos de la trayectoria
def generar_trayectoria():
    for t in np.linspace(0, 10, 100):  # 100 puntos entre 0 y 10
        XA = np.sin(t)  # Ejemplo de trayectoria: funcion seno para X
        YA = np.cos(t)  # Ejemplo de trayectoria: funcion coseno para Y
        trayectoria.append((XA, YA))

# Funcion de actualizacion de la grafica
def actualizar_grafica(frame):
    # Extraemos los puntos de la trayectoria hasta el momento
    x_vals, y_vals = zip(*trayectoria)

    # Limpiar el grafico anterior
    ax.cla()

    # Redibujar el grafico con la nueva trayectoria
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("XA")
    ax.set_ylabel("YA")

    # Graficar la trayectoria
    ax.plot(x_vals, y_vals, label="Trayectoria", color='b')
    if len(trayectoria) > 0:
        XA, YA = trayectoria[-1]
        ax.scatter(XA, YA, color='r', label="Punto actual")
    
    return ax.plot([], [])

# Crear y empezar el hilo para generar la trayectoria
hilo_trayectoria = threading.Thread(target=generar_trayectoria)
hilo_trayectoria.start()

# Crear la animacion
ani = FuncAnimation(fig, actualizar_grafica, frames=100, interval=100)

# Mostrar la grafica
plt.show()

# Esperar a que el hilo termine (opcional)
hilo_trayectoria.join()

