
import cv2
import math
import numpy as np
import mediapipe as mp

import sys
import mediapipe as mp
import math
import tkinter as tk
from tkinter import ttk

import numpy as np
from manos2 import process_hand_frame
# Inicializar MediaPipe para detecn de manos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()









K = np.array([[1701.46226, 0.0, 468.10957],
        [0.0, 1690.89815, 369.38506],
        [0.0, 0.0, 1.0]], dtype=float)

# Coeficientes de distorsión (D)
D = np.array([0.07543864, 0.84724384, 0.01396338, -0.03902927, -1.23286897], dtype=float)

# # Matriz intrínseca y coeficientes de distorsión calibrados
# K = np.array([[724.01480023, 0, 326.76948321],
             # [0, 718.8967463, 320.74633705],
            # [0, 0, 1]], dtype=float)
# D = np.array([-0.2, 0.1, 0, 0, 0])

# Datos para la relación lineal de distancia
distancia_calculada_1 = 100  # cm
distancia_real_1 = 54  # cm
distancia_calculada_2 = 200# cm
distancia_real_2 = 105  # cm



# Ejemplo de uso con la c





# Datos para la relación l
# Ejemplo de uso con la captura de video
#cap = cv2.VideoCapture(0)

from picamera2 import Picamera2




import cv2




import time


last_update_time = time.time()  # Inicializamos el tiempo actual
picam2 = Picamera2()
#picam2.preview_configuration.main.format = "RGB888"  # Establecer formato de color natural
picam2.configure(picam2.create_video_configuration())  # Cambiar a configu de video

print("Inicianmara")
picam2.start()
#time.sleep(2)




while True:





    image = picam2.capture_array()
    ret = image is not None
    frame = image
    if not ret:
        break
    
    frame_ = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

    gesto = ""
    # Procesar la imagen para obtener la posición y distancia
    center_x, center_y, gesto, real_depth = process_hand_frame(mp_hands, mp_drawing, hands, frame_)
    if gesto is not None:
        print(gesto)
    print(gesto)
    
    # Verificar si han pasado más de 0.5 segundos
    current_time = time.time()
    if current_time - last_update_time >= 0.5:
        last_update_time = current_time  # Actualizar el tiempo de la última actualización
        
        # Actualizar valores solo si no son None
        if center_x is not None:
            dx = center_x
        if center_y is not None:
            dy = center_y
        if real_depth is not None:
            dz = real_depth

    if center_x is not None and center_y is not None:
        # Mostrar el resultado en el frame
        cv2.putText(frame_, f"Centro: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_, f"Gesto: {gesto}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame_, f"Distancia Real: {real_depth:.2f} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    
    
    cv2.imshow("mano", frame_)
        
    # Salir con la tecla ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break




picam2.stop()
cv2.destroyAllWindows()
