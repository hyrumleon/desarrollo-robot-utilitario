import cv2
import numpy as np
import math
import cv2.aruco as aruco

from uso_marcadores import calculate_angle, detect_marker_distance_and_angle

# Función principal que maneja la captura de video y la detección en tiempo real
def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
        
        
        
        
        
        
        
            print("Error al capturar el frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Llamar a la función de detección y obtener los resultados
        result = detect_marker_distance_and_angle(gray)

        if result:
            displacement_x_24, displacement_y_24, distance_24, displacement_x_34, displacement_y_34, distance_34, angle_A_degrees = result
            print(f"Displacement 24: {displacement_x_24:.2f}, {displacement_y_24:.2f}, Distance 24: {distance_24:.2f}")
            print(f"Displacement 34: {displacement_x_34:.2f}, {displacement_y_34:.2f}, Distance 34: {distance_34:.2f}")

            print(f"Angle between markers: {angle_A_degrees:.2f} degrees")
        else:
            print("No se detectaron los marcadores 24 y 34.")

        # Mostrar la imagen con los marcadores detectados
        cv2.imshow("ArUco Marker Detection", frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Ejecutar la función principal
if __name__ == "__main__":
    main()
