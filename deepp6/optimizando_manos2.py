import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2

from manos2 import process_hand_frame
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.1, min_tracking_confidence=0.1)

K = np.array([[1701.46226, 0.0, 468.10957], [0.0, 1690.89815, 369.38506], [0.0, 0.0, 1.0]], dtype=float)
D = np.array([0.07543864, 0.84724384, 0.01396338, -0.03902927, -1.23286897], dtype=float)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (320, 180 )}))
picam2.start()

last_update_time = time.time()
frame_counter = 0
process_interval = 1  # Procesar 1 de cada 5 cuadros

while True:
    image = picam2.capture_array()
    frame_ = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    frame_counter += 1
    if frame_counter % process_interval == 0:
        center_x, center_y, gesto, real_depth = process_hand_frame(mp_hands, mp_drawing, hands, frame_)
        
        if center_x and center_y:
            cv2.putText(frame_, f"Centro: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if gesto:
            cv2.putText(frame_, f"Gesto: {gesto}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        if real_depth:
            cv2.putText(frame_, f"Distancia Real: {real_depth:.2f} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Mano", frame_)
    if cv2.waitKey(1) & 0xFF == 27:
        break

picam2.stop()
cv2.destroyAllWindows()
