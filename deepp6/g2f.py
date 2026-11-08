import serial
import time
import re
import matplotlib.pyplot as plt

def agregar_a_lista(elemento, lista_datos):
    """
    Agrega un elemento a la lista de datos si no existe ya, 
    asegurando que no se repitan elementos con el mismo prefijo de dos caracteres.
    """
    # Extraer prefijo (primeros dos caracteres del elemento)
    prefijo = elemento[:2]

    # Revisar si ya existe un elemento con el mismo prefijo en la lista
    if not any(item.startswith(prefijo) for item in lista_datos):
        lista_datos.append(elemento)
        print(f"Elemento '{elemento}' agregado a la lista.")
    
    return lista_datos

def enviar_mensaje(esp32,contador_mensajes, lista_datos):
    """
    Envía un mensaje al puerto serie basado en los argumentos proporcionados.
    El formato del mensaje es: A<contador><argumentos>*.
    """
    contador_mensajes += 1  # Incrementar el contador de mensajes

    # Crear el mensaje comenzando con "A" y el contador
    mensaje = f"A{contador_mensajes}"

    # Agregar los elementos de la lista al mensaje
    for elemento in lista_datos:
        mensaje += str(elemento)

    mensaje += '*'  # Agregar el símbolo de cierre
    esp32.write(mensaje.encode())  # Enviar el mensaje al puerto serie
    print("Mensaje enviado:", mensaje)

    # Vaciar la lista después de enviar el mensaje
    lista_datos.clear()

    return contador_mensajes, lista_datos

def leer_datos(esp32):
    """
    Lee datos del puerto serie y los procesa.
    """
    variables = {}

    if esp32.in_waiting > 0:  # Verificar si hay datos disponibles
        datos_recibidos = esp32.readline().decode('utf-8').strip()  # Leer y decodificar la línea
        print("Datos recibidos:", datos_recibidos)
        
        # Buscar todos los datos en el mensaje recibido
        patrones = re.findall(r'([A-Z]+)([-+]?\d*\.?\d+)', datos_recibidos)
        patrones_extra = re.findall(r'([a-z]+)([-+]?\d*\.?\d+)', datos_recibidos)

        # Actualizar las variables según el identificador
        for identificador, valor in patrones + patrones_extra:
            variables[identificador] = float(valor)

        print(f"Valores asignados: {variables}")

    return variables

def actualizar_grafica(ax, trayectoria, XA, YA):
    """
    Actualiza la gráfica en tiempo real.
    """
    trayectoria.append((XA, YA))

    # Separar los valores de la trayectoria para graficarlos
    x_vals, y_vals = zip(*trayectoria)

    # Limpiar el gráfico anterior
    ax.cla()

    # Redibujar el gráfico con la nueva trayectoria
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("XA")
    ax.set_ylabel("YA")

    # Graficar la trayectoria
    ax.plot(x_vals, y_vals, label="Trayectoria", color='b')
    ax.scatter(XA, YA, color='r', label="Punto actual")

    plt.draw()
    plt.pause(0.01)  # Intervalo para refrescar la gráfica
    
    #time.sleep(0.01)

    return trayectoria

