import cv2
import numpy as np
import math
import cv2.aruco as aruco
# from picamera2 import Picamera2



import time


# Función que calcula el ángulo entre dos marcadores usando la ley de cosenos
def calculate_angle(distance_a, distance_b, distance_c):
    """Calcula el ángulo entre dos puntos dados sus distancias al observador y la distancia entre ellos usando la ley de cosenos."""
    if distance_a <= 0 or distance_b <= 0 or distance_c <= 0:
        raise ValueError("Las distancias deben ser mayores que cero.")
    
    if (distance_a + distance_b <= distance_c or
        distance_a + distance_c <= distance_b or
        distance_b + distance_c <= distance_a):
        raise ValueError("Las distancias no cumplen la desigualdad triangular.")
    
    # Ley de cosenos
    angle_C_radians = math.acos((distance_a**2 + distance_b**2 - distance_c**2) / (2 * distance_a * distance_b))
    
    # Convertir a grados
    angle_C_degrees = math.degrees(angle_C_radians)
    return angle_C_degrees

# Función que detecta los marcadores y calcula las distancias y el ángulo entre ellos
def detect_marker_distance_and_angle(gray):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
    parameters = aruco.DetectorParameters_create()

    # K = np.array([[724.01480023, 0, 326.76948321],
                  # [0, 718.8967463, 320.74633705],
                  # [0, 0, 1]], dtype=float)
    # D = np.array([-0.2, 0.1, 0, 0, 0])
    
    K = np.array([[1701.46226, 0.0, 468.10957],
                [0.0, 1690.89815, 369.38506],
                [0.0, 0.0, 1.0]], dtype=float)

    # Coeficientes de distorsión (D)
    D = np.array([0.07543864, 0.84724384, 0.01396338, -0.03902927, -1.23286897], dtype=float)
    
    K = np.array([[642.6064567,   0,           304.77909356],
              [0,            639.77623171, 233.79004582],
              [0,            0,            1]], dtype=float)

    D = np.array([-0.0837336265, -1.46270316, -0.00823772494, -0.000279533123, 4.54419111], dtype=float)

    real_marker_width_cm = 5# Ancho real del marcador en cm
    m = 1 #0.813  # Pendiente
    b = 0 #2.30   # Intersección
    pixels_per_cm = 10/ 10  # Relación de píxeles a cm

    displacement_x_24 = None
    displacement_y_24 = None
    distance_24 = None

    displacement_x_34 = None
    displacement_y_34 = None
    distance_34 = None

    distance_c = None
    angle_A_degrees = None

    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        aruco.drawDetectedMarkers(gray, corners, ids)

        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, real_marker_width_cm / 100, K, D)

        for i in range(len(ids)):
            aruco.drawAxis(gray, K, D, rvecs[i], tvecs[i], 0.1)
            corner_array = corners[i][0]
            top_left = corner_array[0]
            top_right = corner_array[1]

            detected_width_pixels = int(np.linalg.norm(top_right - top_left))
            distance = (real_marker_width_cm * K[0, 0]) / detected_width_pixels
            x2, y2, x1, y1= 27.67, 52.7, 19.0,  38.4
            x2, y2, x1, y1  = 35.7 , 39.2 , 61.04 , 67.4  
            x2, y2, x1, y1  = 35.7 , 19.6 , 61.04 , 33.7  
            x2, y2, x1, y1  = 146.5 , 33.5, 292.09, 64
            #x2, y2, x1, y1  = 1,1,2,2
    
            
            
            distance = ((y2 - y1) / (x2 - x1)) * (distance - x1) + y1
            #distance = m * distance + b

            marker_center_x = (top_left[0] + top_right[0]) / 2
            marker_center_y = (top_left[1] + corner_array[3][1]) / 2
            
            center_x, center_y = gray.shape[1] // 2, gray.shape[0] // 2
            relative_x = (marker_center_x - center_x)
            relative_y = (marker_center_y - center_y) * -1

            displacement_x = (relative_x / pixels_per_cm)
            displacement_y = (relative_y / pixels_per_cm)

            marker_id = ids[i][0]
            if marker_id == 24:
                displacement_x_24 = displacement_x
                displacement_y_24 = displacement_y
                distance_24 = distance
            elif marker_id == 34:
                displacement_x_34 = displacement_x
                displacement_y_34 = displacement_y
                distance_34 = distance
                
        if displacement_x_24 is not None and displacement_x_34 is not None:
            distance_c = 16
            try:
                angle_A_degrees = calculate_angle(distance_24, distance_34, distance_c)
            except ValueError as e:
                print(f"Error al calcular el ángulo: {e}")

            return (displacement_x_24, displacement_y_24, distance_24,
                    displacement_x_34, displacement_y_34, distance_34, angle_A_degrees)

    return None


# Función principal que maneja la captura de video y la detección en tiempo real
def main():
    

    while True:
    
        #image = picam2.capture_array()
        
        #frame = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer un cuadro.")
            break
       
        #frame_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_ = cv2.resize(frame, (160, 120))

        gray = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)

        # Llamar a la función de detección y obtner los resultados
        result = detect_marker_distance_and_angle(frame_)
        
        if result is not None:  # Por ejemplo, si result no es None
            displacement_x_24, displacement_y_24, distance_24, displacement_x_34, displacement_y_34, distance_34, angle_A_degrees = result
            # if displacement_x_24 is not None and displacement_x_34 is not None:
                # distance = abs(displacement_x_24 - displacement_x_34)
                # x2, y2, x1, y1 = 6.4, 405.5, 6.4, 173.5
                # distance = ((y2 - y1) / (x2 - x1)) * (distance - x1) + y1
                # print(distance)
            print(f"Displacement 24: {displacement_x_24:.2f}, {displacement_y_24:.2f}, Distance 24: {distance_24:.2f}")
            print(f"Displacement 34: {displacement_x_34:.2f}, {displacement_y_34:.2f}, Distance 34: {distance_34:.2f}")
            
            if angle_A_degrees is not None:
                print(f"Angle between markers: {angle_A_degrees:.2f} degrees")
        else:
            print("No se detectaron los marcadores 24 y 34.")

        # Mostrar la imagen con los marcadores detecta
        cv2.imshow("ArUco Marker Detection", frame_)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    picam2.stop()
    
    
    cv2.destroyAllWindows()

# Ejecutar la función principal
if __name__ == "__main__":

    # picam2 = Picamera2()
    # #picam2.preview_configuration.main.format = "RGB888"  # Establecer formato de color natural
    # picam2.configure(picam2.create_video_configuration(main={"size": (640, 360)})) # Cambiar a configu de video
    
    # print("Inicianmara")
    # picam2.start()
    K = np.array([[642.6064567,   0,           304.77909356],
              [0,            639.77623171, 233.79004582],
              [0,            0,            1]], dtype=float)


    D = np.array([-0.0837336265, -1.46270316, -0.00823772494, -0.000279533123, 4.54419111], dtype=float)







    # mara USB (dev/video2)
    cap = cv2.VideoCapture('/dev/video0')
    time.sleep(2)
    
    main()
