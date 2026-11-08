import cv2
import time
import numpy as np

import mediapipe as mp
from picamera2 import Picamera2

from manos2 import process_hand_frame

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define niveles de confianza
min_detection_confidence = 0.1
min_tracking_confidence = 0.1

# Inicializa el modelo de manos
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence
)

K = np.array([[1701.46226, 0.0, 468.10957], [0.0, 1690.89815, 369.38506], [0.0, 0.0, 1.0]], dtype=float)
D = np.array([0.07543864, 0.84724384, 0.01396338, -0.03902927, -1.23286897], dtype=float)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 360)}))
picam2.start()

last_update_time = time.time()
frame_counter = 0
process_interval = 1  # Procesar datos adicionales cada 5 cuadros

# Variables para almacenar el estado de la mano
last_center_x, last_center_y, last_gesto, last_real_depth = None, None, None, None
last_hand_confidence = 0

while True:
    image = picam2.capture_array()
    frame_ = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesar cada cuadro para mantener rastreo
    results = hands.process(frame_)

    if results.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Nivel de confianza actual de la mano
            last_hand_confidence = hand_handedness.classification[0].score

            # Dibuja los puntos de referencia de la mano en el marco
            mp_drawing.draw_landmarks(frame_, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Actualizar informacin adicional cada ciertos cuadros
            frame_counter += 1
            if frame_counter % process_interval == 0:
                # Extrae datos procesados adicionales
                last_center_x, last_center_y, last_gesto, last_real_depth = process_hand_frame(
                    mp_hands, mp_drawing, hands, frame_
                )

    # Mostrar siemp
    if last_center_x and last_center_y:
        cv2.putText(frame_, f"Centro: ({last_center_x}, {last_center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if last_gesto:
        cv2.putText(frame_, f"Gesto: {last_gesto}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    if last_real_depth:
        cv2.putText(frame_, f"Distancia Real: {last_real_depth:.2f} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Mostrar nivel de confianza de la mano detectada
    cv2.putText(frame_, f"Confianza Mano: {last_hand_confidence:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Mano", frame_)
    if cv2.waitKey(1) & 0xFF == 27:
        break

picam2.stop()
cv2.destroyAllWindows()
