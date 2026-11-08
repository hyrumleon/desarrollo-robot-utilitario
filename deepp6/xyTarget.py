import csv
import math
import matplotlib.pyplot as plt  # Importar matplotlib para graficar

# Función para obtener las posiciones de las celdas con valores específicos desde un archivo CSV
def obtener_posiciones_valores_csv(valores_buscar, nombre_archivo="estado_celdas.csv"):
    posiciones = []
    with open(nombre_archivo, mode="r") as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila_idx, fila in enumerate(lector_csv):
            for columna_idx, valor in enumerate(fila):
                if int(valor) in valores_buscar:
                    posiciones.append((fila_idx, columna_idx))
    return posiciones

# Función para convertir posiciones de celdas (fila, columna) a coordenadas X, Y
def convertir_a_coordenadas(posiciones, tamaño_celda=0.125, num_filas=40, num_columnas=40):
    coordenadas = []
    centro_x = (num_columnas * tamaño_celda) / 2
    centro_y = (num_filas * tamaño_celda) / 2
    
    for fila, columna in posiciones:
        # Convertir fila y columna a coordenadas en un plano cartesiano centrado
        x = (columna * tamaño_celda) - centro_x + (tamaño_celda / 2)
        y = centro_y - (fila * tamaño_celda) - (tamaño_celda / 2)
        coordenadas.append((x, y))
    
    return coordenadas

# Función para calcular la distancia entre dos coordenadas (x1, y1) y (x2, y2)
def calcular_distancia(coordenada1, coordenada2):
    x1, y1 = coordenada1
    x2, y2 = coordenada2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Función para crear una lista de coordenadas en orden de distancia más cercana
def obtener_ruta_ordenada(coordenadas_inicio, coordenadas_valor_3_y_4, coordenadas_final):
    ruta = [coordenadas_inicio]
    coordenadas_restantes = coordenadas_valor_3_y_4[:]
    ruta_actual = coordenadas_inicio

    while coordenadas_restantes:
        # Calcular la distancia desde la ruta actual a todas las coordenadas restantes
        distancias = [(coord, calcular_distancia(ruta_actual, coord)) for coord in coordenadas_restantes]
        # Encontrar la coordenada más cercana
        coordenada_cercana, _ = min(distancias, key=lambda x: x[1])
        # Agregar la coordenada más cercana a la ruta
        ruta.append(coordenada_cercana)
        # Eliminar la coordenada más cercana de las restantes
        coordenadas_restantes.remove(coordenada_cercana)
        # Actualizar la coordenada actual
        ruta_actual = coordenada_cercana

    # Finalmente, agregar el punto final
    ruta.append(coordenadas_final)
    
    return ruta

# Función para encontrar el punto de intersección entre el círculo y la ruta
def encontrar_interseccion_circulo_y_ruta(ruta, centro, radio):
    # Descomponer las coordenadas del centro
    centro_x, centro_y = centro
    interseccion = None
    
    # Iterar sobre los segmentos de la ruta
    for i in range(len(ruta) - 1):
        p1 = ruta[i]
        p2 = ruta[i + 1]
        
        # Para cada segmento, calcular la intersección con el círculo
        x1, y1 = p1
        x2, y2 = p2
        
        # Dirección del segmento
        dx = x2 - x1
        dy = y2 - y1
        
        # Ecuación paramétrica del segmento
        a = dx**2 + dy**2
        b = 2 * (dx * (x1 - centro_x) + dy * (y1 - centro_y))
        c = (x1 - centro_x)**2 + (y1 - centro_y)**2 - radio**2
        
        discriminante = b**2 - 4 * a * c
        
        # Si el discriminante es mayor o igual a 0, hay una intersección
        if discriminante >= 0:
            t1 = (-b + math.sqrt(discriminante)) / (2 * a)
            t2 = (-b - math.sqrt(discriminante)) / (2 * a)
            
            # Elegir el valor de t que esté dentro del segmento
            for t in [t1, t2]:
                if 0 <= t <= 1:
                    interseccion_x = x1 + t * dx
                    interseccion_y = y1 + t * dy
                    interseccion = (interseccion_x, interseccion_y)
                    break
        
        if interseccion:
            break
    
    return interseccion

def ejecutar_proceso():

    # Obtener y convertir posiciones de las celdas con valor 1
    posiciones_valor_1 = obtener_posiciones_valores_csv([1], "estado_celdas.csv")
    coordenadas_valor_1 = convertir_a_coordenadas(posiciones_valor_1)

    # Obtener y convertir posiciones de las celdas con valor 2
    posiciones_valor_2 = obtener_posiciones_valores_csv([2], "estado_celdas.csv")
    coordenadas_valor_2 = convertir_a_coordenadas(posiciones_valor_2)

    # Obtener y convertir posiciones de las celdas con valor 3 o 4
    posiciones_valor_3_y_4 = obtener_posiciones_valores_csv([3, 4], "estado_celdas.csv")
    coordenadas_valor_3_y_4 = convertir_a_coordenadas(posiciones_valor_3_y_4)

    # Obtener la ruta ordenada desde el inicio (valor 1) hasta el final (valor 2)
    ruta_ordenada = obtener_ruta_ordenada(coordenadas_valor_1[0], coordenadas_valor_3_y_4, coordenadas_valor_2[0])

    # Definir el radio y el centro del círculo (origen)
    centro_circulo = ruta_ordenada[0]
    radio_circulo = 0.2

    # Encontrar el punto de intersección entre la ruta y el círculo
    punto_interseccion = encontrar_interseccion_circulo_y_ruta(ruta_ordenada, centro_circulo, radio_circulo)



    # Imprimir las coordenadas de la intersección o del punto final si no hay intersección
    if punto_interseccion:
        print(f"Coordenadas de la intersección: {punto_interseccion}")
    else:
        print(f"No se encontró intersección. Coordenadas del punto final: {ruta_ordenada[-1]}")

    # Graficar la ruta
    x_vals = [coord[0] for coord in ruta_ordenada]
    y_vals = [coord[1] for coord in ruta_ordenada]

    # Crear el gráfico
    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='b', label='Ruta ordenada')

    # Dibujar el punto de inicio en verde y el punto final en rojo después de la ruta
    plt.scatter(x_vals[0], y_vals[0], color='g', label='Inicio', zorder=5)  # Punto de inicio en verde
    plt.scatter(x_vals[-1], y_vals[-1], color='r', label='Final', zorder=5)  # Punto final en rojo

    # Dibujar un círculo con el origen en el punto inicial y radio 0.2
    circle = plt.Circle((centro_circulo[0], centro_circulo[1]), radio_circulo, color='orange', fill=False, linestyle='--', label='Círculo con radio 0.2')
    plt.gca().add_patch(circle)

    # Dibujar el punto de intersección en rosa
    if punto_interseccion:
        plt.scatter(punto_interseccion[0], punto_interseccion[1], color='magenta', label='Intersección', zorder=5)

    # # Etiquetas y título
    # plt.title('Ruta ordenada y punto de intersección')
    # plt.xlabel('Coordenada X')
    # plt.ylabel('Coordenada Y')

    # # Hacer la escala de la gráfica uniforme
    # plt.axis('equal')

    # # Mostrar leyenda
    # plt.legend()

    # # Mostrar el gráfico
    # plt.grid(True)
    # plt.show()







if __name__ == "__main__":
    ejecutar_proceso()



