# absl-py               2.1.0
# attrs                 24.2.0
# cffi                  1.17.1
# contourpy             1.3.0
# cycler                0.12.1
# flatbuffers           24.3.25
# fonttools             4.53.1
# jax                   0.4.33
# jaxlib                0.4.33
# kiwisolver            1.4.7
# matplotlib            3.9.2
# mediapipe             0.10.14
# ml_dtypes             0.5.0
# numpy                 2.1.1
# opencv-contrib-python 4.10.0.84
# opencv-python         4.10.0.84
# opt-einsum            3.3.0
# packaging             24.1
# pillow                10.4.0
# pip                   23.2.1
# protobuf              4.25.4
# pycparser             2.22
# pyparsing             3.1.4
# python-dateutil       2.9.0.post0
# scipy                 1.14.1
# setuptools            65.5.0
# six                   1.16.0
# sounddevice           0.5.0

# Python 3.11.5







import mediapipe as mp
import math
import tkinter as tk
from tkinter import ttk

import numpy as np


        
def reconocer_gesto(fingers, thumb_angle, index_angle):
    """
    Reconocer gestos de la mano basados en la extensión de los dedos y ángulos del pulgar e índice.
    
    :param fingers: Lista de enteros [0, 1, 1, 0, 1], donde 1 indica dedo extendido y 0 retraído.
    :param thumb_angle: Ángulo del pulgar en grados.
    :param index_angle: Ángulo del índice en grados.
    :return: Nombre del gesto reconocido.
    """
    
    # ------------------------------
    # Cálculo de ángulos para el pulgar e índice:
    #
    # # Calcular el ángulo del dedo índice (punta 8, base 6)
    # index_angle = get_finger_angle(lmList, finger_tip_id=8, finger_base_id=6)
    # print(f"Ángulo del dedo índice: {index_angle:.2f} grados")
    #
    # # Calcular el ángulo del pulgar (punta 4, base 2)
    # thumb_angle = get_finger_angle(lmList, finger_tip_id=4, finger_base_id=2)
    # print(f"Ángulo del dedo pulgar: {thumb_angle:.2f} grados")
    # ------------------------------

    # Pulgar arriba: Ángulo entre 45° y 135°, pulgar extendido y otros dedos retraídos
    if 45 <= thumb_angle <= 135 and fingers[0] == 1 and all(num == 0 for num in fingers[1:]):
        return "Pulgar arriba: Avanzar o continuar con la acción actual"
    
    # Pulgar abajo: Ángulo entre -45° y -135°, pulgar extendido y otros dedos retraídos
    elif -135 <= thumb_angle <= -45 and fingers[0] == 1 and all(num == 0 for num in fingers[1:]):
        return "Pulgar abajo: Detener o cancelar la acción"
    
    # Pulgar a la derecha: Ángulo entre -45° y 45°, pulgar extendido y otros dedos retraídos
    elif -45 < thumb_angle < 45 and fingers[0] == 1 and all(num == 0 for num in fingers[1:]):
        return "Pulgar a la derecha: Ejecutar acción de giro o cambio a la derecha"
    
    # Pulgar a la izquierda: Ángulo mayor a 135° o menor a -135°, pulgar extendido y otros dedos retraídos
    elif (thumb_angle > 135 or thumb_angle < -135) and fingers[0] == 1 and all(num == 0 for num in fingers[1:]):
        return "Pulgar a la izquierda: Ejecutar acción de giro o cambio a la izquierda"
    
    # Puño cerrado: Todos los dedos retraídos
    elif all(num == 0 for num in fingers):
        return "Puño cerrado: Prepararse para iniciar una nueva tarea o acción"
    
    # V de la victoria: Dedos índice y medio arriba, otros dedos retraídos
    elif fingers[1] == 1 and fingers[2] == 1 and all(num == 0 for num in [fingers[0], fingers[3], fingers[4]]):
        return "V de la victoria: Girar a la derecha"
    
    # Mano abierta: Todos los dedos están arriba
    elif all(num == 1 for num in fingers):
        return "Mano abierta: Detenerse inmediatamente"
    
    # Mano en forma de cuerno: Solo el dedo índice y el meñique están arriba
    elif fingers[1] == 1 and fingers[4] == 1 and all(num == 0 for num in [fingers[0], fingers[2], fingers[3]]):
        return "Mano en forma de cuerno: Cambiar a modo de espera o ahorro de energía"
    
    elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        return "Mano en forma de garra: Cambiar a modo de espera o ahorro de energía"

    # Dedos cruzados: Todos los dedos levantados, asumiendo una función personalizada
    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
        return "Dedos cruzados: Ejecutar una acción especial o programada"
    
    # # Palma levantada: Todos los dedos están extendidos y el pulgar con ángulo entre -135° y -45°
    # elif all(num == 1 for num in fingers) and -135 <= thumb_angle <= -45:
    #     return "Palma levantada: Regresar a la posición de inicio o base"

    
    # Señalar con el dedo índice: Solo el dedo índice está arriba
    elif fingers[1] == 1 and all(num == 0 for num in [fingers[0], fingers[2], fingers[3], fingers[4]]):
        return "Índice arriba: Moverse hacia el lugar señalado"
    
    # # Nuevo gesto: Índice y medio cruzados, otros dedos retraídos
    # elif fingers[1] == 1 and fingers[2] == 1 and all(num == 0 for num in [fingers[0], fingers[3], fingers[4]]):
    #     return "Índice y medio cruzados: Pausar o cambiar de modo"
    
    # Si no se reconoce un gesto
    return "Gesto no reconocido"





# Función para calcular el ángulo entre dos vectores
def calculate_angle3(p1, p2, p3):
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    angle = math.degrees(math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0]))
    return angle

# Función para calcular la distancia euclidiana entre dos puntos 3D
def euclidean_distance2(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)




# Función para determinar si un dedo está extendido o retraído
def is_finger_extended2(hand_landmarks, tip, pip, mcp, cmc=None):
    tip_point = hand_landmarks.landmark[tip]
    pip_point = hand_landmarks.landmark[pip]
    mcp_point = hand_landmarks.landmark[mcp]
    cmc_point = hand_landmarks.landmark[cmc] if cmc else None

    angle_pip_mcp_tip = calculate_angle2(mcp_point, pip_point, tip_point)
    angle_pip_mcp = angle_pip_mcp_tip  # Solo hay un ángulo para dedos si cmc es None
    if cmc:
        angle_mcp_cmc_tip = calculate_angle2(cmc_point, mcp_point, tip_point)
        angle_pip_mcp = angle_mcp_cmc_tip

    return angle_pip_mcp_tip > 160 and angle_pip_mcp > 160




# Función para calcular el ángulo entre tres puntos
def calculate_angle2(a, b, c):
    ab = [a.x - b.x, a.y - b.y, a.z - b.z]
    cb = [c.x - b.x, c.y - b.y, c.z - b.z]
    
    dot_product = ab[0] * cb[0] + ab[1] * cb[1] + ab[2] * cb[2]
    magnitude_ab = math.sqrt(ab[0]**2 + ab[1]**2 + ab[2]**2)
    magnitude_cb = math.sqrt(cb[0]**2 + cb[1]**2 + cb[2]**2)
    
    if magnitude_ab * magnitude_cb == 0:  # Para evitar división por cero
        return 0
    angle = math.acos(dot_product / (magnitude_ab * magnitude_cb))
    return math.degrees(angle)


def process_hand2(hand_landmarks):
    # Obtener el estado del pulgar
    thumb_tip = mp_hands.HandLandmark.THUMB_TIP
    thumb_ip = mp_hands.HandLandmark.THUMB_IP
    thumb_mcp = mp_hands.HandLandmark.THUMB_MCP
    thumb_cmc = mp_hands.HandLandmark.THUMB_CMC
    
    thumb_state, angle_thumb_mcp, angle_thumb_ip, normalized_distance_thumb_tip_mcp = is_thumb_extended2(hand_landmarks)

    # Determinar el estado de los otros dedos
    index_state = "Extendido" if is_finger_extended2(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                                    mp_hands.HandLandmark.INDEX_FINGER_PIP,
                                                    mp_hands.HandLandmark.INDEX_FINGER_MCP) else "Retraído"
    middle_state = "Extendido" if is_finger_extended2(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                                                     mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                                                     mp_hands.HandLandmark.MIDDLE_FINGER_MCP) else "Retraído"
    ring_state = "Extendido" if is_finger_extended2(hand_landmarks, mp_hands.HandLandmark.RING_FINGER_TIP,
                                                   mp_hands.HandLandmark.RING_FINGER_PIP,
                                                   mp_hands.HandLandmark.RING_FINGER_MCP) else "Retraído"
    pinky_state = "Extendido" if is_finger_extended2(hand_landmarks, mp_hands.HandLandmark.PINKY_TIP,
                                                    mp_hands.HandLandmark.PINKY_PIP,
                                                    mp_hands.HandLandmark.PINKY_MCP) else "Retraído"

    return thumb_state, index_state, middle_state, ring_state, pinky_state, angle_thumb_mcp, angle_thumb_ip, normalized_distance_thumb_tip_mcp

def is_thumb_extended2(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]

    angle_thumb_mcp = calculate_angle2(thumb_cmc, thumb_mcp, thumb_ip)
    angle_thumb_ip = calculate_angle2(thumb_mcp, thumb_ip, thumb_tip)
    distance_thumb_tip_mcp = euclidean_distance2(thumb_tip, thumb_mcp)

    # Utiliza la distancia entre MCP del pulgar y MCP del índice como referencia
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    reference_distance = euclidean_distance2(thumb_mcp, index_mcp)

    # Normalizar la distancia del pulgar
    normalized_distance_thumb_tip_mcp = distance_thumb_tip_mcp / reference_distance

    angle_threshold = 155
    distance_threshold = 0.65  # Ajusta este valor según la escala de tus coordenadas

    angle_check = angle_thumb_mcp > angle_threshold and angle_thumb_ip > angle_threshold
    distance_check = normalized_distance_thumb_tip_mcp > distance_threshold
    
    thumb_state = "Extendido" if angle_check and distance_check else "Retraído"
    
    return thumb_state, angle_thumb_mcp, angle_thumb_ip, normalized_distance_thumb_tip_mcp

# Función para calcular el ángulo entre tres puntos
def calculate_angle(a, b, c):
    ab = [a.x - b.x, a.y - b.y, a.z - b.z]
    cb = [c.x - b.x, c.y - b.y, c.z - b.z]
    
    dot_product = ab[0] * cb[0] + ab[1] * cb[1] + ab[2] * cb[2]
    magnitude_ab = math.sqrt(ab[0]**2 + ab[1]**2 + ab[2]**2)
    magnitude_cb = math.sqrt(cb[0]**2 + cb[1]**2 + cb[2]**2)
    
    if magnitude_ab * magnitude_cb == 0:  # Para evitar división por cero
        return 0
    angle = math.acos(dot_product / (magnitude_ab * magnitude_cb))
    return math.degrees(angle)



# Función para calcular la distancia entre dos puntos
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Función para verificar la distancia entre el pulgar e índice
def verify_thumb_index_distance(landmarks):
    thumb_tip = landmarks[4]  # Punta del pulgar
    index_finger_tip = landmarks[8]  # Punta del dedo índice
    wrist = landmarks[0]  # Muñeca

    # Calcular la distancia entre las puntas del dedo índice y pulgar
    dist_thumb_index = calculate_distance(thumb_tip, index_finger_tip)
    # Calcular la distancia de la muñeca a la punta del dedo índice
    dist_wrist_index = calculate_distance(wrist, index_finger_tip)

    # Normalizar la distancia entre el pulgar e índice en relación con la distancia de la muñeca a la punta del dedo índice
    normalized_distance = dist_thumb_index / dist_wrist_index if dist_wrist_index > 0 else 0
    return normalized_distance

# gesto_detector.py

import numpy as np
import mediapipe as mp

# Inicializar MediaPipe para la detección de manos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

def process_hand_frame(mp_hands , mp_drawing, hands, frame_rgb):
    """
    Función que procesa el frame para obtener:
    - El centro del recuadro de la palma (coordenadas X, Y).
    - El gesto de la mano detectada.
    - La distancia real calculada de la mano.
    """
    
    
    
    
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
    
    distancia_calculada_1 = 80  # cm
    distancia_real_1 = 50  # cm
    distancia_calculada_2 = 150  # cm
    distancia_real_2 = 120  # cm

    # Calcular pendiente (m) y la intersección (b)
    m = (distancia_real_2 - distancia_real_1) / (distancia_calculada_2 - distancia_calculada_1)
    b = distancia_real_1 - m * distancia_calculada_1

        # Conversión de BGR a RGB para MediaPipe
        
        
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        hand_labels = []
        for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
            # Dibuja las conexiones de la mano
            mp_drawing.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_labels.append(f"MANO{idx + 1}")

            # Obtener las coordenadas del recuadro de la palma (base de los dedos)
            landmarks = hand_landmarks.landmark
            h, w, _ = frame_rgb.shape
            
            # Coordenadas de los dedos índice y pulgar
            thumb_tip = (landmarks[mp_hands.HandLandmark.THUMB_TIP].x * w, landmarks[mp_hands.HandLandmark.THUMB_TIP].y * h)
            index_tip = (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w, landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)
            wrist = (landmarks[mp_hands.HandLandmark.WRIST].x * w, landmarks[mp_hands.HandLandmark.WRIST].y * h)

            # Calcular los ángulos
            thumb_angle = calculate_angle3(wrist, thumb_tip, (thumb_tip[0] + 1, thumb_tip[1]))
            index_angle = calculate_angle3(wrist, index_tip, (index_tip[0] + 1, index_tip[1]))
            

            base_finger_x = [landmarks[i].x for i in [0, 5, 9, 13, 17]]
            base_finger_y = [landmarks[i].y for i in [0, 5, 9, 13, 17]]

            # Escalar las coordenadas de los puntos
            base_finger_x = [int(x * w) for x in base_finger_x]
            base_finger_y = [int(y * h) for y in base_finger_y]

            # Calcular las coordenadas del cuadrado usando la base de los dedos
            x_min_base = min(base_finger_x)
            x_max_base = max(base_finger_x)
            y_min_base = min(base_finger_y)
            y_max_base = max(base_finger_y)

            # Calcular el ancho del rectángulo
            width_rect = x_max_base - x_min_base

            # Definir el ancho real del objeto en cm
            W_real = 8.7  # Ancho real en cm

            # Calcular la profundidad estimada utilizando la distancia focal
            f = K[0, 0]  # Distancia focal (en píxeles)
            estimated_depth = (f * W_real) / width_rect if width_rect > 0 else float('inf')  # Profundidad en cm

            # Aplicar la relación lineal para calcular la profundidad real
            real_depth = m * estimated_depth + b

            # Calcular la posición del cuadrado
            square_size = int(width_rect * 1.5)  # Ajusta el multiplicador según sea necesario

            # Calcular la posición del cuadrado
            square_x_min = (x_min_base + x_max_base) // 2 - square_size // 2
            square_x_max = (x_min_base + x_max_base) // 2 + square_size // 2
            square_y_min = (y_min_base + y_max_base) // 2 - square_size // 2
            square_y_max = (y_min_base + y_max_base) // 2 + square_size // 2

            # Calcular el centro del recuadro
            square_center_x = (square_x_min + square_x_max) // 2
            square_center_y = (square_y_min + square_y_max) // 2
            
             # Verificar los estados de los dedos
            
            thumb_state, index_state, middle_state, ring_state, pinky_state, angle_thumb_mcp, angle_thumb_ip, normalized_distance_thumb_tip_mcp = process_hand2(hand_landmarks)

            # Imprimir estado de los dedos
            finger_states = [pinky_state, ring_state, middle_state, index_state, thumb_state]
            
        
            fingers = ''.join("1" if state == "Extendido" else "0" for state in finger_states[::-1])  # Invertir el orden de los dedos
            gesto = reconocer_gesto([int(f) for f in fingers], thumb_angle, index_angle)

            return square_center_x, square_center_y, gesto, real_depth

    return None, None, None, None  # Si no se detecta mano, retornar valores nulos
