# -*- coding: utf-8 -*-
from picamera2 import Picamera2
import time
import numpy as np
import cv2

picam2 = Picamera2()
#picam2.preview_configuration.main.format = "RGB888"  # Establecer formato de color natural
picam2.configure(picam2.create_video_configuration())  # Cambiar a configu de video

print("Inicianmara")
picam2.start()
time.sleep(2)

# Bucle para capturar y mostrar video en tiempo real
try:
    while True:
        # Capturar un frame
        image = picam2.capture_array()

        # Imprimir las dimensiones de la imagen
        print(f"Dimensiones de la imagen: {image.shape}")

        # Convertir de RGBA a BGR
        frame_bgr3 = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

        # Convertir de BGR a escala de grises
        gray_image = cv2.cvtColor(frame_bgr3, cv2.COLOR_BGR2GRAY)

        # Redimensionar la imagen para hacer la ventana 
        small_image = cv2.resize(gray_image, (640, 360))  # Cambia el ta

        # Mostrar el frame en escala de grises
        cv2.imshow("Video en Escala de Grises", small_image)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    # Manejar la interrup del teclado
    pass

# Detener lamara y cerrar ventanas
print("Deteniendo cmara")
picam2.stop()
cv2.destroyAllWindows()
