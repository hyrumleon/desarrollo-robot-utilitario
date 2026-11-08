import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import pygame
import sys
from depth_anything.inference import DepthAnythingInference
from a_star31 import *

# Configuración de la cámara
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)

# Función para reiniciar la cuadrícula
def reset_grid(grid, start, end):
    
    grid, start, end = [], None, None
    for i in range(rows):
        row_nodes = []
        for j in range(cols):
            node = Node(grid, j, i)
            row_nodes.append(node)
        grid.append(row_nodes)
    
    return grid, start, end
    
    









def set_start_end_from_input(command, rows , cols, grid):
    parts = command.split(',')
    if len(parts) == 6 and parts[0] == "inicio" and parts[3] == "fin":
        start_row, start_col = int(parts[1]), int(parts[2])
        end_row, end_col = int(parts[4]), int(parts[5])

        if (0 <= start_row < rows and 0 <= start_col < cols and
            0 <= end_row < rows and 0 <= end_col < cols):
            start = grid[start_row][start_col]
            end = grid[end_row][end_col]
            return start, end  # Regresa los valores de start y end
        else:
            print("Error: Las posiciones de inicio o fin están fuera del rango permitido.")
    return None, None  # Retorna None si los valores no son válidos

# Función para dibujar paredes basándose en los valores de profundidad

def draw_walls_from_line_values(line_values, rows , cols, grid, start , end):
    grid = clear_walls(rows , cols, grid, start , end)
    line_length = len(line_values)
    scale_factor = line_length / cols

    for col in range(3, 37):  # Este rango puede modificarse según sea necesario
        mapped_index = int(col * scale_factor)
        mapped_value = line_values[mapped_index]
        #print(mapped_value)
        row = int((1 - (mapped_value / 255)) * (rows - 1))

        if 1 < row < rows - 12:
            # Agregar muro en la celda central
            grid[row][col].type = 'wall'
            for offset in range(1, 4):  # Agregar muros hacia abajo
                if row + offset < rows - 3:
                    grid[row + offset][col].type = 'wall'

            # Agregar muros a los lados de la celda central
            if col > 1:  # Verificar que no se salga del límite izquierdo
                grid[row][col - 1].type = 'wall'  # Muro a la izquierda
                for offset in range(1, 4):  # Agregar muros hacia abajo en la columna izquierda
                    if row + offset < rows - 3:
                        grid[row + offset][col - 1].type = 'wall'
            
            if col < cols - 2:  # Verificar que no se salga del límite derecho
                grid[row][col + 1].type = 'wall'  # Muro a la derecha
                for offset in range(1, 4):  # Agregar muros hacia abajo en la columna derecha
                    if row + offset < rows - 3:
                        grid[row + offset][col + 1].type = 'wall'


# Función para limpiar las paredes
def clear_walls(  rows , cols, grid, start , end):
    for i in range(rows):
        for j in range(cols):
            grid[i][j].type = 'empty'
    return grid

# Función para realizar la búsqueda de camino
def pathfind(rows , cols, grid, start , end):
    if not start or not end:
        print('Por favor, marca los nodos de inicio y fin.')
        return None  # Retorna None si no hay nodos de inicio o fin

    path = a_star(grid, start, end)
    if not path:
        print('No hay rutas posibles.')
        return None  # Retorna None si no hay ruta

    # Actualizar el tipo de los nodos en la ruta
    for node in path:
        if node != start and node != end:
            node.type = 'path'
            
            
    
    
    

    # Calcular la distancia y el ángulo
    distance = round(path[-1].f_score, 2)
    if distance % 1 == 0:
        distance = int(distance)
    print('Ruta encontrada con distancia de ' + str(distance) + '.')

    if len(path) >= 6:
        third_node = path[5]
        angle = calculate_angle(start, third_node)
        print(f'Ángulo desde el nodo de inicio al tercer nodo: {angle:.2f} grados')
        return angle  # Retorna el ángulo calculado
    else:
        print('No hay suficientes nodos en la ruta para calcular el ángulo.')
        return None  # Retorna None si no hay suficientes nodos

# Función para calcular ángulo
def calculate_angle(start_node, target_node):
    delta_x = target_node.x - start_node.x
    delta_y = target_node.y - start_node.y
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

# Bucle principal de procesamiento de fotogramas
def frame_processing():
    cap = cv2.VideoCapture(0)
    low_res_size = (40, 30)  # Tamaño reducido para el procesamiento




    # Configuración de DepthAnything
    depth_anything = DepthAnythingInference(model_path='depth_anything/models/depth_anything_vits14.onnx', color=True)


    line_number = 15  # Ajustado para la resolución reducida





    rows = 40
    cols = 40
    grid = []
    start = None
    end = None
    
    
    
    
    
    grid , start , end = reset_grid(grid, start, end)
    command = "inicio,0,20,fin,39,20"
    
    
    start, end = set_start_end_from_input(command , rows , cols, grid)



    while True:
        t = cv2.waitKey(5)
        ret, frame = cap.read()
        if not ret:
            break
        
        
        
        
        
        
        
        
        
        
        
        

        

        h, w, _ = frame.shape

            

        print(f'{h} {w}')
        #print("Rows:", rows, "Cols:", cols)




        # Reducir resolución para el modelo
        low_res_frame = cv2.resize(frame, low_res_size)
        img_depth = depth_anything.frame_inference(low_res_frame)

        # Convertir a escala de grises
        gray_depth = cv2.cvtColor(img_depth, cv2.COLOR_BGR2GRAY)
        depth_values = gray_depth[line_number, :]  # Línea horizontal completa
        
        
        

        draw_walls_from_line_values(depth_values, rows , cols, grid, start , end)

        cv2.line(frame, (0, int(line_number * 16)), (640, int(line_number * 16)), (0, 255, 0), 2)
        cv2.imshow('depth anything', gray_depth)
        cv2.imshow('frame in real time', frame)

        angle = pathfind(rows , cols, grid, start , end)
        print(angle)




        if t == 27:  # Presiona Esc para salir
            break

    cap.release()
    cv2.destroyAllWindows()
    plt.ioff()
    plt.show()

# # Inicialización
# reset_grid()
# command = "inicio,0,20,fin,39,20"
# set_start_end_from_input(command)

if __name__ == "__main__":
    frame_processing()
