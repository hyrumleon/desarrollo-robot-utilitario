
from picamera2 import Picamera2




import cv2




import time
picam2 = Picamera2()
#picam2.preview_configuration.main.format = "RGB888"  # Establecer formato de color natural
picam2.configure(picam2.create_video_configuration())  # Cambiar a configu de video

print("Inicianmara")
picam2.start()
time.sleep(2)
    

import numpy as np
import matplotlib.pyplot as plt
import math
import pygame
import sys
from depth_anything.inference import DepthAnythingInference





from a_star31 import *


from anguloE import draw_walls_from_line_values , pathfind , reset_grid, set_start_end_from_input


low_res_size = (80, 45)  # Tamaño reducido para el procesamiento




# Configuración de DepthAnything
depth_anything = DepthAnythingInference(model_path='depth_anything/models/depth_anything_vits14.onnx', color=True)


line_number = 22  # Ajustado para la resolución reducida





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
    
    
    
    image = picam2.capture_array()
        
    frame = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        
    
    
    
    
    
    
    

    

    h, w, _ = frame.shape

        

    print(f'{h} {w}')
    
    
    




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
    print(angle)




    if t == 27:  # Presiona Esc para salir
        break





picam2.stop()
cv2.destroyAllWindows()




