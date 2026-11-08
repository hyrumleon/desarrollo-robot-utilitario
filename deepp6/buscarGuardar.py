import pygame
import csv
from a_star11 import *



#pygame.init()

# Variables globales
rows = 40
cols = 40
grid = []
start = None
end = None
walls = {}

def guardar_estado_csv2(nombre_archivo="estado_celdas.csv"):
    global start, end, walls, grid
    with open(nombre_archivo, mode="w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        for i in range(rows):
            fila = []
            for j in range(cols):
                node = grid[i][j]
                if node == start:
                    fila.append(1)  # Celda de inicio
                elif node == end:
                    fila.append(2)  # Celda de fin
                elif node.type == 'path' and (i, j) in walls:
                    fila.append(4)  # Intersección de ruta y muro
                elif node.type == 'path':
                    fila.append(3)  # Celda como parte de la ruta
                elif (i, j) in walls:
                    fila.append(5)  # Muro
                else:
                    fila.append(0)  # Celda vacía
            escritor_csv.writerow(fila)
    print("Estado de la cuadrícula guardado en", nombre_archivo)

def leer_estado_csv(nombre_archivo="estado_celdas.csv", *args):
    global start, end, walls, grid
    with open(nombre_archivo, mode="r") as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for y, fila in enumerate(lector_csv):
            for x, valor in enumerate(fila):
                valor = int(valor)
                if valor in args:  # Solo procesa valores que están en los argumentos
                    node = grid[y][x]  # Obtener la celda de la cuadrícula
                    if valor == 1:
                        start = node
                    elif valor == 2:
                        end = node
                    elif valor == 3:
                        node.type = 'path'  # Marca como parte de la ruta
                    elif valor == 4:
                        walls[(y, x)] = node
                        node.type = 'path'  # Intersección de ruta y muro
                    elif valor == 5:
                        walls[(y, x)] = node
                        node.type = 'wall'  # Marca como muro
                else:
                    grid[y][x].type = 'road'  # Limpia las celdas no incluidas en args
                
                
    print(f"Estado de la cuadrícula cargado desde {nombre_archivo} con filtros {args}")
    




    
    
    
    
    
    
    
    
    # Imprime todos los datos de la cuadrícula (grid) después de cargar
    print("\nDatos de la cuadrícula:")
    # for row in grid:
    #     for node in row:
    #         print(f"({node.x}, {node.y}) -> {node.type}")
    
    # Imprime el estado de las otras variables
    print("\nEstado de las otras variables:")
    print(f"Start: {start}")
    print(f"End: {end}")
    #print(f"Walls: {walls}")
def reset_grid():
    global grid, start, end, walls
    grid, start, end, walls = [], None, None, {}
    for i in range(rows):
        row_nodes = []
        for j in range(cols):
            node = Node(grid, j, i)
            row_nodes.append(node)
        grid.append(row_nodes)

def pathfind():
    if not start or not end:
        print('Please mark both endpoint nodes.')
        return
    path = a_star(grid, start, end)
    if not path:
        print('No possible paths.')
        return
    else:
        distance = round(path[-1].f_score, 2)
        if distance % 1 == 0:
            distance = int(distance)
        print('Path found with distance ' + str(distance) + '.')
    for node in path:
        if node != start and node != end:
            node.type = 'path'

# Función principal
def ejecutar_búsqueda():
    reset_grid()  # Reinicia la cuadrícula
    leer_estado_csv("estado_celdas.csv", 1, 2, 3, 4, 5)  # Cargar el archivo con los filtros correspondientes
    pathfind()  # Ejecuta la búsqueda A*
    guardar_estado_csv2("estado_celdas.csv")  # Guarda el estado de la cuadrícula al final

if __name__ == "__main__":
    ejecutar_búsqueda()