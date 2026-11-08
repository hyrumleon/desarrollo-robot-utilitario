import cv2
import time
import numpy as np
import mediapipe as mp

from manos2 import process_hand_frame

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.1, min_tracking_confidence=0.1)

K = np.array([[1701.46226, 0.0, 468.10957], [0.0, 1690.89815, 369.38506], [0.0, 0.0, 1.0]], dtype=float)
D = np.array([0.07543864, 0.84724384, 0.01396338, -0.03902927, -1.23286897], dtype=float)
K = np.array([[642.6064567,   0,           304.77909356],
              [0,            639.77623171, 233.79004582],
              [0,            0,            1]], dtype=float)

D = np.array([-0.0837336265, -1.46270316, -0.00823772494, -0.000279533123, 4.54419111], dtype=float)







# mara USB (dev/video2)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir lmara.")
    exit()




# Obtener el tamano nativo del cuadro antes de establecerlo
native_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
native_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(f"Tamano nativo de la camara: {int(native_width)}x{int(native_height)}")

# Establecer el tamano deseado
width = 160   # Puedes ajustar esto
height = 120  # Puedes ajustar esto
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Obtener el tamano actual despues de la configuracion
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(f"Tamano actual de la imagen capturada despues de configurar: {int(frame_width)}x{int(frame_height)}")


frame_counter = 0
process_interval = 1  # Procesar 1 de cada 5 cuadros

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer un cuadro.")
        break
   
    #frame_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_ = cv2.resize(frame, (160, 120))
    frame_counter += 1
    if frame_counter % process_interval == 0:
        center_x, center_y, gesto, real_depth = process_hand_frame(mp_hands, mp_drawing, hands, frame_)
        
        if center_x and center_y:
            cv2.putText(frame_, f"Centro: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 2)
        if gesto:
            cv2.putText(frame_, f"Gesto: {gesto}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 0, 0), 2)
        if real_depth:
            cv2.putText(frame_, f"D: {real_depth:.2f} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

    cv2.imshow("Mano", frame_)
    
    # Detener al presionar 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Liberar laara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
