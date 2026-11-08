
#  0 para celdas vacías,
# 1 para celdas de inicio,
# 2 para celdas de fin,
# 3 para celdas en la ruta,
# 4 para intersección de ruta y muro,
# 5 para muros.


import pygame, math, sys
from a_star11 import *

pygame.init()
pygame.font.init()

HEIGHT = 800
WIDTH = 800

display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = ((int(135 * 0.7), int(206 * 0.7), int(250 * 0.7)))  # Color especial para las intersecciones

font = pygame.font.SysFont('Arial', 10)
text1 = font.render('Start/End Node (Right Click)', False, BLACK)
text2 = font.render('Wall Node (Left Click)', False, BLACK)
text3 = font.render('Start', False, WHITE)
text4 = font.render('Undo', False, WHITE)
text5 = font.render('Clear', False, WHITE)
text6 = font.render('Toggle Wall Mode', False, WHITE)  # Texto para el botón de alternancia
text_save = font.render('Save', False, WHITE)  # Texto para el botón de guardar

text_load = font.render('Load', False, WHITE)  # Texto para el botón de cargar

icon = pygame.image.load(r'/home/pi/Desktop/HYRUM/arucooo/deepp/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Pathfinder')

import csv




def guardar_estado_csv(nombre_archivo="estado_celdas.csv" ):
    global start, end, walls, grid
    with open(nombre_archivo, mode="w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        for i in range(rows):
            fila = []
            for j in range(cols):
                node = grid[i][j]
                
                #print("node.type:", node.type)  # Verifica el valor de node.type
                    
                    
                    
                    
                    
                if node == start:
                    
                    fila.append(1)  # Celda de inicio
                    print("61")
                elif node == end:
                    fila.append(2)  # Celda de fin
                    print("62") 
                elif node.type == 'path' and (i, j) in walls:
                    print("63")
                    fila.append(4)  # Intersección de ruta y muro
                elif node.type == 'path':
                    print("node.type:", node.type)  # Verifica el valor de node.type
                    
                    
                    fila.append(3)  # Celda como parte de la ruta
                    print("64")
                elif (i, j) in walls:
                    fila.append(5)  # Muro
                    print("65")
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
                    print(valor)
                    
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
    update_grid(display, grid)
    print(f"Estado de la cuadrícula cargado desde {nombre_archivo} con filtros {args}")



def update_display():
    display.fill(WHITE)
    pygame.draw.rect(display, BLUE, (10, 5, 10, 10))
    pygame.draw.rect(display, BLACK, (200, 5, 10, 10))
    display.blit(text1, (25, 5))
    display.blit(text2, (215, 5))

    # Buttons
    pygame.draw.rect(display, BLACK, (355, 7, 40, 10))
    pygame.draw.rect(display, BLACK, (435, 7, 40, 10))
    pygame.draw.rect(display, BLACK, (515, 7, 40, 10))
    pygame.draw.rect(display, (0, 255, 0) if wall_mode else (255, 0, 0), (595, 7, 100, 10))
    print("272")
    pygame.draw.rect(display, BLACK, (715, 7, 40, 10))  # Botón de guardar
    pygame.draw.rect(display, BLACK, (765, 7, 40, 10))  # Botón de cargar

    display.blit(text3, (362, 6))
    display.blit(text4, (443, 6))
    display.blit(text5, (524, 6))
    display.blit(text6, (605, 6))
    display.blit(text_save, (722, 6))
    display.blit(text_load, (772, 6))  # Texto del botón de cargar

rows = 40
cols = 40
grid = []
undo_log = []
start = None
end = None
walls = {}  # Diccionario para almacenar las coordenadas de los muros
wall_mode = True  # Modo de muro: True para agregar, False para borrar

def reset_grid():
    global grid, start, end, undo_log, walls
    grid, undo_log, start, end, walls = [], [], None, None, {}  # Reiniciar los muros también

    for i in range(rows):
        row_nodes = []
        for j in range(cols):
            node = Node(grid, j, i)
            row_nodes.append(node)
        grid.append(row_nodes)
    update_grid(display, grid)

def update_grid(display, grid):
    update_display()
    rect_width = (WIDTH - 1) / cols
    rect_height = (HEIGHT - 21) / cols

    for i in range(rows):
        for j in range(cols):
            color = None
            node = grid[i][j]
            if (i, j) in walls:  # Verifica si la coordenada está en el diccionario de muros
                color = BLACK
            elif node == start:
                color = (0, 255, 0)  # Verde para el nodo de inicio
            elif node == end:
                color = (128, 0, 128)  # Morado para el nodo de fin
            elif node.type == 'path':
                color = LIGHT_BLUE
                print("node.type:", node.type)  # Verifica el valor de node.type

            # Si el nodo está en la intersección de muro y ruta, cambia el color
            if (i, j) in walls and node.type == 'path':
                color = RED  # Color especial para intersección de ruta y muro

            if color:
                pygame.draw.rect(display, color, (j * rect_width + 1, i * rect_height + 21, rect_width, rect_height))

    for i in range(len(grid) + 1):
        pygame.draw.rect(display, GRAY, (i * rect_width, 20, 1, HEIGHT))
        pygame.draw.rect(display, GRAY, (0, i * rect_height + 20, WIDTH, 1))

    pygame.display.update()

reset_grid()
update_grid(display, grid)

def clear_path_nodes():
    for i in range(rows):
        for j in range(cols):
            node = grid[i][j]
            if node.type == 'path':  # Solo borra nodos de tipo 'path'
                node.type = 'road'
                print("p")

def draw_tile(x, y, tile_type):
    global start, end, undo_log, walls
    clear_path_nodes()
    print("204")  
    row = ((y - 20) * rows) // (HEIGHT - 20)
    col = (x * cols) // WIDTH
    node = grid[row][col]

    if row < 0 or col < 0 or row >= rows or col >= cols or node.type == 'wall' or node == start or node == end:
        return
    elif tile_type == 'endpoint' and start and end:
        return

    if tile_type == 'wall':
        grid[row][col].type = 'wall'
        walls[(row, col)] = True  # Guardar las coordenadas del muro en el diccionario
    elif tile_type == 'endpoint':
        if not start:
            start = node
        elif not end:
            end = node

    undo_log.append(node)
    update_grid(display, grid)

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
    update_grid(display, grid)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Test for click on start, undo, clear, toggle wall, save, and load buttons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos[0], mouse_pos[1]

            if 355 <= x <= 395 and 7 <= y <= 17:  # Botón de iniciar
                pathfind()
            elif 435 <= x <= 475 and 7 <= y <= 17:  # Botón de deshacer
                if undo_log:
                    node = undo_log.pop()
                    node.type = 'road'
                    if node == start or node == end:
                        if end:
                            end = None
                        elif start:
                            start = None
                    update_grid(display, grid)
            elif 515 <= x <= 555 and 7 <= y <= 17:  # Botón de limpiar
                reset_grid()
            elif 595 <= x <= 695 and 7 <= y <= 17:  # Botón de alternancia de muro
                print("272")
                wall_mode = not wall_mode
            elif 715 <= x <= 755 and 7 <= y <= 17:  # Botón de guardar
                guardar_estado_csv("estado_celdas.csv")
            elif 765 <= x <= 805 and 7 <= y <= 17:  # Botón de cargar
                leer_estado_csv("estado_celdas.csv", 1, 2, 3,4, 5)  # Cargar con filtros 1, 2, 3, 5

        # Right click adds start/end node
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos[0], mouse_pos[1]
            print("282")
            
            # Verifica si las coordenadas (x, y) no están dentro del rango del botón de cargar
            if not ((765 <= x <= 805 and 7 <= y <= 17) or 
            (715 <= x <= 755 and 7 <= y <= 17) or 
            (355 <= x <= 395 and 7 <= y <= 17)):
                print("282")
                draw_tile(x, y, 'endpoint')

        # Left click adds or removes wall node based on wall_mode state
        if pygame.mouse.get_pressed()[0]:
            print("289")
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos[0], mouse_pos[1]

            if wall_mode:
                print("291")
                if not ((765 <= x <= 805 and 7 <= y <= 17) or 
                (715 <= x <= 755 and 7 <= y <= 17) or 
                (355 <= x <= 395 and 7 <= y <= 17)):
                    print("282")
                    draw_tile(x, y, 'wall')
            else:
                row = ((y - 20) * rows) // (HEIGHT - 20)
                col = (x * cols) // WIDTH
                if (row, col) in walls:
                    del walls[(row, col)]
                    grid[row][col].type = 'road'
                update_grid(display, grid)