import csv

# Función para cargar el estado de la cuadrícula desde un archivo CSV
def cargar_estado_csv(nombre_archivo="estado_celdas.csv"):
    estado_celdas = []
    with open(nombre_archivo, mode="r", newline="") as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            estado_celdas.append([int(valor) for valor in fila])
    return estado_celdas

# Función para actualizar el estado de una celda
def actualizar_estado_celda(estado_celdas, x, y, estado):
    num_filas = len(estado_celdas)
    num_columnas = len(estado_celdas[0]) if num_filas > 0 else 0
    if 0 <= x < num_columnas and 0 <= y < num_filas:
        estado_celdas[y][x] = estado
    else:
        print(f"Posición ({x}, {y}) fuera de los límites de la cuadrícula.")

# Función para guardar el estado de la cuadrícula en un archivo CSV
def guardar_estado_csv(estado_celdas, nombre_archivo="estado_celdas.csv"):
    with open(nombre_archivo, mode="w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        for fila in estado_celdas:
            escritor_csv.writerow(fila)

# Función para mapear la posición (X, Y) a la celda correspondiente
def mapear_posicion_a_celda(X, Y, tamaño_celda=0.125, num_filas=40, num_columnas=40):
    centro_x = (num_columnas * tamaño_celda) / 2
    centro_y = (num_filas * tamaño_celda) / 2
    columna = int((X + centro_x) // tamaño_celda)
    fila = int((Y + centro_y) // tamaño_celda)
    if 0 <= columna < num_columnas and 0 <= fila < num_filas:
        return fila, columna
    else:
        return None

# Función para agregar o actualizar un estado en la cuadrícula dado X, Y y un valor de estado
def agregar_estado(estado_celdas, X, Y, estado, tamaño_celda=0.125, num_filas=40, num_columnas=40):
    if 0 <= estado <= 5:
        resultado = mapear_posicion_a_celda(X, Y, tamaño_celda, num_filas, num_columnas)
        if resultado:
            fila, columna = resultado
            actualizar_estado_celda(estado_celdas, columna, fila, estado)
            print(f"Estado {estado} actualizado en la posición ({X}, {Y}) -> Fila {fila}, Columna {columna}")
        else:
            print(f"Posición ({X}, {Y}) fuera de los límites de la cuadrícula.")
    else:
        print("El estado debe estar entre 0 y 5.")

# Función para borrar valores específicos en la cuadrícula
def borrar_valores(estado_celdas, valores_a_borrar):
    for y, fila in enumerate(estado_celdas):
        for x, valor in enumerate(fila):
            if valor in valores_a_borrar:
                estado_celdas[y][x] = 0  # Se reemplaza el valor por 0
    guardar_estado_csv(estado_celdas, "estado_celdas.csv")
    print(f"Valores {valores_a_borrar} borrados de la cuadrícula y guardados en el archivo.")

# Función para reemplazar un valor específico en la cuadrícula
def reemplazar_valor(estado_celdas, valor_original, valor_nuevo):
    for y, fila in enumerate(estado_celdas):
        for x, valor in enumerate(fila):
            if valor == valor_original:
                estado_celdas[y][x] = valor_nuevo
    guardar_estado_csv(estado_celdas, "estado_celdas.csv")
    print(f"Valores {valor_original} reemplazados con {valor_nuevo} en la cuadrícula y guardados en el archivo.")



def main():
    # Cargar el estado de la cuadrícula desde el archivo CSV existente
    estado_celdas = cargar_estado_csv("estado_celdas.csv")

    # Ejemplo de uso para reemplazar el valor 4 con 5
    valor_original = 0
    valor_nuevo = 3
    reemplazar_valor(estado_celdas, valor_original, valor_nuevo)

# Ejecutar el main solo si este script se ejecuta directamente
if __name__ == "__main__":
    main()