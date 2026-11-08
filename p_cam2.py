import os

import sys


#os.system(r'C:\Users\leonl\Downloads\arauco2\env\Scripts\activate && cd C:\Users\leonl\Downloads\arauco2\deepp && python p10__.py')

#sys.path.append(r'C:\Users\leonl\Downloads\arauco2\deepp')
import threading# Función para manejar la captura de la cámara



def actualizar_variables(variables):
    global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA, SA, SB, SP, TL
    M = variables.get('M', M)
    A = variables.get('A', A)
    CA = variables.get('CA', CA)
    AM = variables.get('AM', AM)
    dz = variables.get('dz', dz)
    dx = variables.get('dx', dx) 
    dy = variables.get('dy', dy)
    g = variables.get('g', g)
    XA = variables.get('XA', XA)
    YA = variables.get('YA', YA)
    XB = variables.get('XB', XB)
    YB = variables.get('YB', YB)
    PA = variables.get('PA', PA)
    SA = variables.get('SA', SA)
    SB = variables.get('SB', SB)  # Retrieve 'SB' from 'variables' or use the current value of SB if not found
    SP = variables.get('SP', SP)  # Similarly, retrieve 'SP'
    #TL = variables.get('TL', TL)  # Similarly, retrieve 'TL'

    
    


def captura_camara():
    
    global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA , gesto, nombres, dxcar, dycar, z_car,  bandera_mano, bandera_carro, bandera_cocina, bandera_cuarto, bandera_sala, bandera_aseo, bandera_comedor, bandera_luz , angle
    
    
    import cv2
    import math
    import numpy as np
    import mediapipe as mp

    import sys
    import mediapipe as mp
    import math
    import tkinter as tk
    from tkinter import ttk
    
    import time

    import numpy as np
    from manos2 import process_hand_frame
    # Inicializar MediaPipe para detección de manos
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands =  mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)


##############################################################################################################
    # Ruta de la base de datos de rostros
    path = r'C:\Users\leonl\Downloads\arauco2\DEEPp5\deepp6\know_faces'

    from rostross import procesar_frame , cargar_base_datos , codrostros, procesar_frame2


    # Cargar base de datos inicial
    images, classes = cargar_base_datos(path)
    rostroscod = codrostros(images)

    # Cargar el clasificador Haar
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    start_time = None
####################################################################################################################

    from uso_marcadores import calculate_angle, detect_marker_distance_and_angle


##############################################################################################
    
    
        
    from depth_anything.inference import DepthAnythingInference



    #############################################################################333#

    from anguloE import draw_walls_from_line_values , pathfind , reset_grid, set_start_end_from_input
    low_res_size = (80, 45)  # Tamaño reducido para el procesamiento
    #low_res_size = (40, 30)  # Tamaño reducido para el procesamiento
    # Configuración de DepthAnything
    depth_anything = DepthAnythingInference(model_path='depth_anything/models/depth_anything_vits14.onnx', color=True)
    line_number = 22
    #line_number = 15  # Ajustado para la resolución reducida

    rows = 40
    cols = 40
    grid = []
    start = None
    end = None


    grid , start , end = reset_grid(grid, start, end)
    command = "inicio,0,20,fin,39,20"


    start, end = set_start_end_from_input(command , rows , cols, grid)
#####################################################################################

    from intentar_cali import realizar_calculos
    ########################################################################
    
    from objetos import process_frame


    prototxt = "MobileNetSSD_deploy.prototxt.txt"
    
    model = "MobileNetSSD_deploy.caffemodel"
    classes2 = {
        0: "background", 1: "aeroplane", 2: "bicycle",
        3: "bird", 4: "boat", 5: "bottle", 6: "bus",
        7: "car", 8: "cat", 9: "chair", 10: "cow",
        11: "diningtable", 12: "dog", 13: "horse",
        14: "motorbike", 15: "person", 16: "pottedplant",
        17: "sheep", 18: "sofa", 19: "train", 20: "tvmonitor"
    }
    net = cv2.dnn.readNetFromCaffe(prototxt, model)



    # Matriz de la cámara (K)
    K = np.array([[1701.46226, 0.0, 468.10957],
                [0.0, 1690.89815, 369.38506],
                [0.0, 0.0, 1.0]], dtype=float)

    # Coeficientes de distorsión (D)
    D = np.array([0.07543864, 0.84724384, 0.01396338, -0.03902927, -1.23286897], dtype=float)
    
    K = np.array([[642.6064567,   0,           304.77909356],
              [0,            639.77623171, 233.79004582],
              [0,            0,            1]], dtype=float)

    D = np.array([-0.0837336265, -1.46270316, -0.00823772494, -0.000279533123, 4.54419111], dtype=float)
    
    # Matriz intrínseca y coeficientes de distorsión calibrados
    # K = np.array([[724.01480023, 0, 326.76948321],
                # [0, 718.8967463, 320.74633705],
                # [0, 0, 1]], dtype=float)
    # D = np.array([-0.2, 0.1, 0, 0, 0])
    last_update_time = time.time()  # Inicializamos el tiempo actual


    # Datos para la relación l
    # Ejemplo de uso con la captura de video
    #cap = cv2.VideoCapture(0)
    
    # from picamera2 import Picamera2
    
    
    
    
    import cv2
    
    
    
    
    
    
    import time
    
    
    
    # mara USB (dev/video2)
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: No se pudo abrir lmara.")
        exit()
    #picam2 = Picamera2()
    
    
    #picam2.preview_configuration.main.format = "RGB888"  # Establecer formato de color natural
    #picam2.configure(picam2.create_video_configuration(main={"size": (320, 180)}))
    
    print("Inicianmara")
    #picam2.start()
    #time.sleep(2)
    
    center_x = None
    center_y = None
    
    
    
    # last_update_time = time.time()
    # frame_counter = 0
    # process_interval = 5  # Procesar 1 de cada 5 cuadros

    # while True:
        # image = picam2.capture_array()
        # frame_ = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # frame_counter += 1
        # if frame_counter % process_interval == 0:
            # center_x, center_y, gesto, real_depth = process_hand_frame(mp_hands, mp_drawing, hands, frame_)
            
            # if center_x and center_y:
                # cv2.putText(frame_, f"Centro: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # if gesto:
                # cv2.putText(frame_, f"Gesto: {gesto}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            # if real_depth:
                # cv2.putText(frame_, f"Distancia Real: {real_depth:.2f} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # cv2.imshow("Mano", frame_)
        # if cv2.waitKey(1) & 0xFF == 27:
            # break
    # picam2.stop()
   
    # cv2.destroyAllWindows()
    while True:
    
    
    
    
    
    
    
        # image = picam2.capture_array()
        # ret = image is not None
        # frame = image
        # if not ret:
            # break
        
        
        
    # frame = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        ret, frame__ = cap.read()
        if not ret:
            print("Error: No se pudo leer un cuadro.")
            break
       
        #frame_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_ = cv2.resize(frame__, (160, 120))
        frame_ = cv2.flip(frame_ , 1)
        
        # while cap.isOpened():
        
        # ret, frame = cap.read()
        # if not ret:
            # break

        # Corrección de distorsión
        #frame_undistorted = cv2.undistort(frame, K, D)
        
        # # Convertir de RGBA a BGR
        # frame_bgr3 = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

        # Conversión de BGR a RGB para Mediapipe
        #frame_rgb = cv2.cvtColor(frame_undistorted, cv2.COLOR_BGR2RGB)
        #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = frame_
        frame_undistorted = frame_
        frame = frame_
        
        #gray = cv2.cvtColor(frame ,cv2.COLOR_BGR2GRAY)
        
        #estimar_AE = True
        #bandera_objeto = False
        if bandera_objeto:
            
            low_res_frame = cv2.resize(frame, low_res_size)
            img_depth = depth_anything.frame_inference(low_res_frame)

            # Convertir a escala de grises
            gray_depth = cv2.cvtColor(img_depth, cv2.COLOR_BGR2GRAY)
            depth_values = gray_depth[line_number, :]  # Línea horizontal completa
            
            
            
            





            draw_walls_from_line_values(depth_values, rows , cols, grid, start , end)

            cv2.line(frame, (0, int(line_number * 8)), (640, int(line_number * 8)), (0, 255, 0), 2)
            cv2.imshow('depth anything', gray_depth)
            #cv2.imshow('frame in real time', frame)

            angle = pathfind(rows , cols, grid, start , end)
            print(angle)
        # Llamar a la función de detección y obtener los resultados
        
        result = None
        result = detect_marker_distance_and_angle(frame)


        if result:
            displacement_x_24, displacement_y_24, distance_24, displacement_x_34, displacement_y_34, distance_34, angle_A_degrees = result
            print(f"Displacement 24: {displacement_x_24:.2f}, {displacement_y_24:.2f}, Distance 24: {distance_24:.2f}")
            print(f"Displacement 34: {displacement_x_34:.2f}, {displacement_y_34:.2f}, Distance 34: {distance_34:.2f}")

            print(f"Angle between markers: {angle_A_degrees:.2f} degrees")
            coordenada_X, coordenada_Y, angulo_Z_grados = realizar_calculos(a7 = .16 , a3 =  distance_34 / 100  , a9 =  distance_24 / 100 , t7 = 0, a1 = .6 , a2 = .05)

            print("\nResultado final:")
            print(f"Coordenada X: {coordenada_X}")
            print(f"Coordenada Y: {coordenada_Y}")
            print(f"Ángulo en Z: {angulo_Z_grados}")
        # else:
            
        #     print("No se detectaron los marcadores 24 y 34.")
            
      
        
        
        
        
        
        frame, start_time, images, rostroscod, classes, nombres = procesar_frame2(frame, images, rostroscod, classes, start_time, path, face_cascade)
    
        
        gesto_ = ""
        real_depth = None
        if bandera_mano:
            
            center_x, center_y, gesto, real_depth = process_hand_frame(mp_hands, mp_drawing, hands, frame)

        
        # Verificar si han pasado más de 0.5 segundos
        current_time = time.time()
        if current_time - last_update_time >= 0.5:
            last_update_time = current_time  # Actualizar el tiempo de la última actualización
            
            
                    # Procesar la imagen para obtener la posición y distancia
            #enter_x, center_y, gesto, real_depth = process_hand_frame(mp_hands, mp_drawing, hands, frame)
        
            # Actualizar valores solo si no son None
            if center_x is not None:
                dx = center_x
            else:
                dx = 80
                
            if center_y is not None:
                dy = center_y
                
            if real_depth is not None:
                dz = real_depth
            else:
                dz = 50
            gesto = gesto_
            
                
            

        if center_x is not None and center_y is not None:
            # Mostrar el resultado en el frame
            cv2.putText(frame, f"Centro: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .25, (0, 255, 0), 2)
            cv2.putText(frame, f"Gesto: {gesto}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, .25, (255, 0, 0), 2)
            cv2.putText(frame, f"d: {real_depth:.2f} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        #bandera_carro = True
        if bandera_carro:
        
            # Procesar el cuadro
            detections = process_frame(frame, net, classes2)

            # Imprimir las detecciones
            print("---------------------------------------")
            for obj in detections:
                print(f"Objeto detectado: {obj['label']}")
                print(f"Confianza: {obj['confidence'] * 100:.2f}%")
                print(f"Coordenadas: {obj['box']}")
                print(f"Centro: {obj['center']}")
                
                if obj['label'] == "car": 
                    
                    
                    x_start, y_start, x_end, y_end = obj['box']
                    dxcar = (x_start + x_end) / 2
                    dycar = (y_start + y_end) / 2
                    

                    # Calcular el ancho en píxeles
                    width = x_end - x_start
                    print(f"dxcar {dxcar:.2f}Ancho en píxeles: {width}")
                    
                    # Definir los puntos dados
                    x2, y2, x1, y1= 66, .5, 29, 1
                    x = width
                
                    # Calcular y en una sola línea
                    z_car = ((y2 - y1) / (x2 - x1)) * (x - x1) + y1
                    
                    # Mostrar el resultado
                    
                    print(f"Cuando x = {x}, y = {z_car}")
                    
                    
                    
                    
                    
                    
                    cv2.putText(frame, f"z: {z_car:.2f}", 
                                (x_start, y_end + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    cv2.putText(frame, f"x: {dxcar}", 
                                (x_start, y_end + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                else:
                    dxcar = None
                    dycar = None
                    z_car = None

                    
           
                # Dibujar en el cuadro
                x_start, y_start, x_end, y_end = obj['box']
                cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
                cv2.putText(frame, f"{obj['label']} ({obj['confidence'] * 100:.2f}%)",
                            (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Mostrar el frame
        #cv2.imshow("Frame", frame_undistorted)
        cv2.imshow("Reconocimiento Facial", cv2.resize(frame, (640, 480)))
        

        # Salir con la tecla ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
                
    #picam2.stop()
    cap.release()
    
    cv2.destroyAllWindows()




# Función para manejar la lectura/escritura en el puerto serial
def manejar_serial():
    global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA , gesto, SA, SB, nombres, dxcar, dycar, z_car, SP, TL
    #M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA = [0] * 13  # Inicializar en 
    import serial
    import time
    import math
    
    import numpy as np
    
    from scipy.interpolate import CubicSpline

    import re
    import matplotlib.pyplot as plt
    
    #sys.path.append(r'C:\Users\leonl\Downloads\arauco2\deepp')
    print(dz)
    from g2f import  agregar_a_lista, enviar_mensaje , leer_datos, actualizar_grafica
    
    
    from pxy12T import manejar_busqueda
#####################################################################################################
    
    # Configuración del puerto y la velocidad de transmisión
    port = 'COM16'
    baud_rate = 9600
    puerto_serial = '/dev/rfcomm0'
    baud_rate = 115200

    puerto = '/dev/ttyUSB0'
    puerto = '/dev/ttyACM0'
    #puerto = 'COM11'   
    baudrate2 = 115200





    
    puerto_1 = '/dev/ttyUSB0'
    #puerto_1     = '/dev/ttyACM0'
    puerto_2 = '/dev/rfcomm0'
    puerto_1 = "COM10"
    puerto_2 = "COM7"
    puerto_1 = "COM6"
    puerto_2 = "COM3"
    baud_rate = 115200

    def conectar_puerto(puerto, baud_rate):
        while True:
            print(f"Conectando al puerto {puerto}...")  # Mensaje constante mientras intenta conectar
            try:
                ser = serial.Serial(puerto, baud_rate, timeout=1)
                print(f"Conectado al puerto {puerto}")
                return ser
            except serial.SerialException as e:
                print(f"Error al conectar al puerto {puerto}: {e}. Intentando nuevamente...")
                time.sleep(2)
    
    # Definir la funcin para estimar radianes desde radianes de entrada usando interpolacn cbica
    def estimar_radianes(radianes_input):
        # 1. Definir los puntos de referencia (radianes y grados)
        radianes = np.array([0.0, 1.7, 2.95, 4.41, 2 * np.pi])  # Incluyendo 2*pi para completar el crculo
        grados = np.array([0, 90, 180, 270, 360])  # Grados correspondientes (360 para 2*pi rad)
    

    
    
        # 2. Realizar la interpolacn cbica
        cs = CubicSpline(radianes, grados)  # Interpolacin d radianes a grados

        # 3. Estimar el valor de grados para el valor dado en radianes
        grados_estimados = cs(radianes_input)
        
        # 4. Convertir el valor estimado de grados a radianes
        radianes_estimados = grados_estimados * (np.pi / 180)  # Convierte de grados a radianes
        
        return radianes_estimados
    def ejecutars(esp32_2, esp32):
        global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA , gesto, SA, SB,  bandera_mano, bandera_carro, bandera_cocina, bandera_cuarto, bandera_sala, bandera_aseo, bandera_comedor, bandera_luz, bandera_aseora_objeto, SP, angle , z_car , dxcar

        # Intervalo de tiempo en segundos entre envíos
        intervalo_envio = .218 # 318
        ultimo_envio = time.time()

        # Contador de mensajes enviados
        contador_mensajes = 0

        # Inicializamos la lista que se utilizará para almacenar los datos
        lista_datos = []
        trayectoria = []

        # Inicializar figura para graficar
        # fig, ax = plt.subplots()
        # ax.set_xlim(-3, 3)
        # ax.set_ylim(-3, 3)
        # ax.set_xlabel("XA")
        # ax.set_ylabel("YA")
        
        SA = -1.0
        SB = -1.0
        SP = 0
        dx = 80
        dz = 50
        dxcar = 80
        z_car = .5
        angle = 90
    
        while True:
            try:
                # # Leer datos de puerto 1
                # if ser_1.in_waiting > 0:
                    # linea_1 = ser_1.readline().decode('utf-8', errors='replace').strip()
                    # print(f"Puerto 1: {linea_1}")

                # # Leer datos de puerto 2
                # if ser_2.in_waiting > 0:
                    # linea_2 = ser_2.readline().decode('utf-8', errors='replace').strip()
                    # print(f"Puerto 2: {linea_2}")
                
                        # Enviar datos en intervalos
                if time.time() - ultimo_envio >= intervalo_envio:
                    xt, yt, CT = (1, 0, True) if bandera_cocina else \
                      (1, 1, True) if bandera_cuarto else \
                      (0, 1, True) if bandera_sala else \
                      (-1,  -1, True) if bandera_aseo else \
                      (-1, 0, True) if bandera_comedor else (None, None, 0)
                    
                    
                    
                    
                            
                    if XA is not None and YA is not None and  xt is not None and yt is not None and CT is not None:
                        if -2.5 <  XA < 2.5 and -2.5 < YA < 2.5:  # Verifica si XA y YA están dentro del rango
                            print(f"XA: {XA}, -YA: {YA}, xt: {xt}, -yt: {yt}, bool(CT): {bool(CT)}")
        
        
        
        
        
        
                            XB, YB = manejar_busqueda(XA, YA, xt, yt, bool(CT))
                            if XB is not None and YB is not None:
                                 
                                print("Coordenadas 1:", XB)
                                print("Coordenadas 2:", YB)
                                lista_datos = agregar_a_lista(f"XD{XB:.2f}", lista_datos)
                                lista_datos = agregar_a_lista(f"YD{YB:.2f}", lista_datos)
                                lista_datos = agregar_a_lista("CT1", lista_datos)
                                
                            else:
                                lista_datos = agregar_a_lista("CT0", lista_datos)
                                print("Las coordenadas XA y YA están fuera del rango permitido.")
                    contador_mensajes, lista_datos = enviar_mensaje(esp32, contador_mensajes, lista_datos)
                    ultimo_envio = time.time()
    
                # Agregar elementos a la lista
                #lista_datos = agregar_a_lista("dx2", lista_datos)
                lista_datos = agregar_a_lista("AS0.0", lista_datos)
                lista_datos = agregar_a_lista("BS0.0", lista_datos)
                # lista_datos = agregar_a_lista(f"XD-0.0", lista_datos) 
                # lista_datos = agregar_a_lista(f"YD0.5", lista_datos)
                # lista_datos = agregar_a_lista("CT0", lista_datos)
                if bandera_objeto:
                    lista_datos = agregar_a_lista(f"AE{( math.radians(angle)):.2f}", lista_datos)
                    lista_datos = agregar_a_lista(f"CE{int(bandera_objeto)}", lista_datos)
                    
                
                #lista_datos = agregar_a_lista("CS0", lista_datos)
                

                if bandera_luz:
                    lista_datos = agregar_a_lista(f"TL1", lista_datos)
                else:
                    lista_datos = agregar_a_lista(f"TL0", lista_datos)
                
               
                #bandera_mano = True
                #bandera_carro =True
                
                if (gesto is not None and (
                    "Mano en forma de garra: Cambiar a modo de espera o ahorro de energía" in gesto or 
                    "Mano en forma de cuerno: Cambiar a modo de espera o ahorro de energía" in gesto ) or dx is not None and dz is not None and bandera_mano is not False) or (dxcar is not None and z_car is not None and bandera_carro is not False):
                        
                    
                    #ndera_carro = False
                
                    #andera_mano  = False
                    #print(bandera_mano)
                    #print(bandera_carro)
                    #bandera_mano = True
                    if bandera_carro:
                        if dxcar is not None:
                        
                        
                    
                    
                            lista_datos = agregar_a_lista(f"dx{dxcar:.2f}", lista_datos)
                            lista_datos = agregar_a_lista(f"dz{z_car:.2f}", lista_datos)
                            lista_datos = agregar_a_lista("CS1", lista_datos)
                        else:
                            lista_datos = agregar_a_lista("CS0", lista_datos)
                    elif bandera_mano:
                        
                        lista_datos = agregar_a_lista(f"dx{dx:.2f}", lista_datos)
                        lista_datos = agregar_a_lista(f"dz{dz/100:.2f}", lista_datos)
                        lista_datos = agregar_a_lista("CS1", lista_datos)
        
                else:
                    
                    lista_datos = agregar_a_lista("CS0", lista_datos)
                    
                    
                    
                    
                
        
                # Leer datos recibidos  
                variables = leer_datos(esp32)
                variables2 = leer_datos(esp32_2)
                if variables:
                    actualizar_variables(variables)
                    print(f"Datos actualizados: M={M}, A={A}, CA={CA}, AM={AM}, dz={dz}, dx={dx}, dy={dy}, g={g}, XA={XA}, YA={YA}, XB={XB}, YB={YB}, PA={PA}")
                    #trayectoria = actualizar_grafica(ax,trayectoria, XA, YA)
                    
                    
                    
                    # xt , yt , CT  = 1.6, 1, 1
                    
                    
                    # if XA is not None and YA is not None:
                        # if -2.5 <  XA < 2.5 and -2.5 < YA < 2.5:  # Verifica si XA y YA están dentro del rango
                            # print(f"XA: {XA}, -YA: {-YA}, xt: {xt}, -yt: {-yt}, bool(CT): {bool(CT)}")
        
                            # XB, YB = manejar_busqueda(XA, -YA, xt, -yt, bool(CT))
                            # print("Coordenadas 1:", XB)
                            # print("Coordenadas 2:", YB)
                        # else:
                            # print("Las coordenadas XA y YA están fuera del rango permitido.")
        
                
                if variables2:
                    actualizar_variables(variables2)
                    print(f"Datos actualizados: SA = {SA}, SB = {SB}, SP = {SP}")
        
        
        
            
        
        
                agregar_a_lista(f"SA{SA}", lista_datos)
                agregar_a_lista(f"SB{SB}", lista_datos)
                
                #agregar_a_lista(f"SP{SP}", lista_datos)
                SP_ = estimar_radianes(SP)
                agregar_a_lista(f"SP{SP_:.2f}", lista_datos)
                #agregar_a_lista(f"TL{TL}", lista_datos)
                
                
                

            except (serial.SerialException, OSError) as e:
                print(f"Error en la cone: {e}. Cerrando conexiones y reiniciando...")
                esp32_2.close()
                esp32.close()
                return False
            except KeyboardInterrupt:
                print("\nLectura interrumpida por el usuario.")
                esp32_2.close()
                esp32.close()
                exit(0)
                
                
                
    while True:
        try:
            # Conectar a los puertos por separado
            print("Conectando al puerto 1...")
            
            esp32_2 = conectar_puerto(puerto_1, baud_rate)

            print("Conectando al puerto 2...")
            esp32 = conectar_puerto(puerto_2, baud_rate)

            # Leer datos de ambos puertos
            if not ejecutars(esp32_2, esp32):
                time.sleep(2)  # Esperamos antes de intentar nuevamente
        except Exception as e:
            print(f"Error inesperado: {e}. Reiniciando...")
            time.sleep(2)
      
        
        # esp32 = verificar_conexion(esp32, puerto_serial, baud_rate)
        # esp32_2 = verificar_conexion(esp32_2, puerto, baudrate2)

        # # Si alguna con falla, intentar nuevamente
        # if not esp32 or not esp32_2:
            # print("Reconexin fallida. Reintentando...")
            # time.sleep(3)
            # continue

        
        

        # #time.sleep(.1)
    


        
        
        


# Función para manejar comandos de voz
def manejar_voz():
    global nombres ,  bandera_mano, bandera_carro, bandera_cocina, bandera_cuarto, bandera_sala, bandera_aseo, bandera_comedor, bandera_luz
    
        
    from escuchar import escuchar_comando0 , confirmar_tarea, procesar_comando , grabar_audio_durante_10_seg, escuchar_comando
    
    from sintetizar_pi import hablar
    
    from sintetizar12 import hablar2
    
    
     #enciende la luz
    #siguiendo la palma de la mano
    #siguiendo el automovil
    #transporta esto a la cocina
    #transportando habitacion
    #llevando a la sala
    #llevando al bano
    #llevando al comedor
    tareas = {
        "encender_luz": "Encendiendo la luz...",
        "apagar_luz": "Apagando la luz...",
        "seguir_mano": "Siguiendo la mano...",
        "detener_seguir_mano": "Deteniendo la tarea de seguir mano...",
        "seguir_carro": "Siguiendo el automovil...",
        "detener_seguir_carro": "Deteniendo la tarea de seguir carro...",
        "transportar_cocina": "Transportando a la cocina...",
        "transportar_cuarto": "Transportando al cuarto...",
        "transportar_sala": "Transportando a la sala...",
        "transportar_aseo": "Transportando al aseo...",
        "transportar_comedor": "Transportando al comedor...",
        "evadir_objeto": "Evitando colision con un objeto..."
    }

    # Palabras clave de acciones (con sinonimos)
    palabras_clave = {
        "encender_luz": {"verbo": ["encender", "prender"], "sustantivo": ["luz", "foco", "poco"]},
        "apagar_luz": {"verbo": ["apagar"], "sustantivo": ["luz", "foco", "lampara", "poco"]},
        "seguir_mano": {"verbo": ["seguir"], "sustantivo": ["mano"]},
        "detener_seguir_mano": {"verbo": ["detener", "parar", "dejar"], "sustantivo": ["seguir", "mano"]},
        "seguir_carro": {"verbo": ["seguir"], "sustantivo": ["automovil" , "carro"]},
        "detener_seguir_carro": {"verbo": ["detener", "parar"], "sustantivo": ["seguir", "carro"]},
        "transportar_cocina": {"verbo": ["ve", "llevar" ,"transportar"], "sustantivo": ["cocina", "fogon"]},
        "transportar_cuarto": {"verbo": ["ve","llevar" , "transportar"], "sustantivo": ["cuarto", "habitación"]},
        "transportar_sala": {"verbo": ["ve", "lleva" , "transportar"], "sustantivo": ["sala", "estancia"]},
        "transportar_aseo": {"verbo": ["ve", "llevar" , "transportar"], "sustantivo": ["bano", "aseo"]},
        "transportar_comedor": {"verbo": ["ve","llevar" , "transportar"], "sustantivo": ["comedor", "refrectorio"]},
         "evadir_objeto": {"verbo": ["evadir", "esquivar", "evitar"], "sustantivo": ["objeto", "obstaculo", "colision"]}
    }




    from colorama import Fore, Style






    # Lista de palabras que indican negación
    palabras_negacion = ["evitar", "cancelar", "dejar", "parar", "no"]

    # Lista de palabras que indican "alto" y sinónimos
    palabras_alto = ["alto", "detente", "parar", "detener", "alto ahí"]


    # Lista de palabras que indican "sí" y "no"
    palabras_si = ["sí", "si", "claro", "por supuesto", "afirmativo"]
    palabras_no = ["no", "negativo", "para nada", "nada"]
    
    
    
    ##############################################################################
    
    
    
    import RPi.GPIO as GPIO
    import time

    BUTTON_GPIO = 24
    LED_GPIO = 23

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_GPIO, GPIO.OUT)
    GPIO.output(LED_GPIO, False)
    
    
    print("Procesando comandos de voz...")



    while True:
        time.sleep(0.2)  # Espera un corto periodo para evitar un uso excesivo de CPU

        # Implementar la lógica de reconocimiento de voz aquí
        #print("Procesando comandos de voz...")
        
        if GPIO.input(18) == GPIO.LOW:
            low_count += 1
            print(f"Pin 18 esta en LOW! (Conteo: {low_count})")
            
            if low_count >= 5:
                GPIO.output(15, GPIO.LOW)
                print("Pin 15 esta apagado (LOW)!")
                
                GPIO.cleanup()
                os.system("sudo shutdown now")
                sys.exit()

        else:
            low_count = 0
        
        if nombres :
            
            hablar2(str(f"hola{nombres[0]}") , velocidad = 70)

        if GPIO.input(BUTTON_GPIO) == GPIO.HIGH:
            hablar("Escuchando" , velocidad = 70)
            GPIO.output(LED_GPIO, True)
            print("LED encendido.")
            comando = escuchar_comando()
            GPIO.output(LED_GPIO, False)
            print("LED apagado.")
            if comando is not None:
                print(Fore.GREEN + comando)
            print(Style.RESET_ALL + "Texto normal.")
            if comando:
                tarea = procesar_comando(comando, palabras_clave , palabras_alto )
                
                
                
                
                
                if tarea == "alto":
        
                    bandera_mano = False
                    bandera_carro = False
                    bandera_cocina = False
                    bandera_cuarto = False
                    bandera_sala = False
                    bandera_aseo = False
                    bandera_comedor = False
                    bandera_objeto = False
                    
                    bandera_luz = False  # Nueva bandera para encender luz
                        
                            
                    print("Bandera 'Alto' activada. Todas las otras tareas detenidas.")
                    hablar2(str(f"Alto"), velocidad = 70)
                    #return  # Salir de la función después de activar la bandera "alto"
                    
                if tarea in tareas:
                    
                    if tarea == "seguir_mano":
                        bandera_mano = True
                    elif tarea == "seguir_carro":
                        bandera_carro = True
                    elif tarea == "transportar_cocina":
                        bandera_cocina = True
                    elif tarea == "transportar_cuarto":
                        bandera_cuarto = True
                    elif tarea == "transportar_sala":
                        bandera_sala = True
                    elif tarea == "transportar_aseo":
                        bandera_aseo = True
                    elif tarea == "transportar_comedor":
                        bandera_comedor = True
                    elif tarea == "encender_luz":
                        bandera_luz = True  # Activar la bandera para encender luz
                    elif tarea == "apagar_luz":
                        bandera_luz = False
                    elif tarea == "evadir_objeto":
                        bandera_objeto = True
                        
                    hablar2(str(f" '{tareas[tarea]}'?"), velocidad = 70)
            
                
                    
                    # print(f"¿Deseas ejecutar la tarea: '{tareas[tarea]}'? (Di 'sí' o 'no')")
                    # hablar2(str(f"¿Deseas ejecutar la tarea: '{tareas[tarea]}'" ), velocidad = 70)
                    # GPIO.output(LED_GPIO, True)
                    # respuesta = escuchar_comando()  # Esperar la respuesta del usuario
                    # GPIO.output(LED_GPIO, False)
                    # if comando is not None:
                        # print(Fore.GREEN + comando)
                    # print(Style.RESET_ALL + "Texto normal.")
    
                    # if respuesta is not None:
                        # if confirmar_tarea(respuesta, palabras_si , palabras_no):  # Pregunta al usuario si desea ejecutar la tarea
                            # print(tareas[tarea])
                            
                            # # MANEJAR TAREAS
                            
                            
                                                # # Inicializa todas las banderas en False
                            # bandera_mano = False
                            # bandera_carro = False
                            # bandera_cocina = False
                            # bandera_cuarto = False
                            # bandera_sala = False
                            # bandera_aseo = False
                            # bandera_comedor = False
                            # bandera_luz = False  # Nueva bandera para encender luz
                        
                            # # Activa icamente la bandera correspondiente
                            # if tarea == "seguir_mano":
                                # bandera_mano = True
                            # elif tarea == "seguir_carro":
                                # bandera_carro = True
                            # elif tarea == "transportar_cocina":
                                # bandera_cocina = True
                            # elif tarea == "transportar_cuarto":
                                # bandera_cuarto = True
                            # elif tarea == "transportar_sala":
                                # bandera_sala = True
                            # elif tarea == "transportar_aseo":
                                # bandera_aseo = True
                            # elif tarea == "transportar_comedor":
                                # bandera_comedor = True
                            # elif tarea == "encender_luz":
                                # bandera_luz = True  # Activar la bandera para encender luz
                            
                            # hablar2(str(f" '{tareas[tarea]}'?"), velocidad = 70)
                                
                                
                    # else:
                        # print("Tarea cancelada por el usuario.")
                elif tarea == "no_tarea":
                    print("No se ejecutará ninguna tarea debido a la negación.")
                else:
                    
                    
                    print("No se pudo identificar la tarea.")

            
            

# Declarar todas las variables globales
global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA, gesto, bandera_mano, bandera_carro, bandera_cocina, bandera_cuarto, bandera_sala, bandera_aseo, bandera_comedor, bandera_luz, bandera_objeto, TL , SP, dx_car

M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA = [0] * 13
dz = 80
dx = 50
dx_car = .5

gesto = ""

nombres = None


bandera_mano = True
bandera_carro = False
bandera_cocina = False
bandera_cuarto = False
bandera_sala = False
bandera_aseo = False
bandera_comedor = False
bandera_objeto = False
    
bandera_luz = False  



#import RPi.GPIO as GPIO
import time

# # Configura los pines
# GPIO.setmode(GPIO.BCM)  # Usa la numeracin de pines BCM
# GPIO.setup(18, GPIO.IN)  # Configura el pin 18 como entrada
# GPIO.setup(15, GPIO.OUT)  # Configura el pin 15 como salida
# GPIO.output(15, GPIO.LOW)

print("Esperando a que el pin 18 esta en HIGH...")

# # Espera hasta que el pin 18 est en HIGH
# while GPIO.input(18) == GPIO.LOW:
#     time.sleep(0.1)  # Espera un corto periodo para evitar un uso excesivo de CPU

print("Pin 18 esta en HIGH!")

# # Enciende el pin 15 (lo pone en HIGH)
# GPIO.output(15, GPIO.HIGH)
print("Pin 15 esta en HIGH!")

# Crear los hilos
hilo_camara = threading.Thread(target=captura_camara)
hilo_serial = threading.Thread(target=manejar_serial)
# hilo_voz = threading.Thread(target=manejar_voz)

import time
# Iniciar los hilos
hilo_camara.start() 
time.sleep(20)
hilo_serial.start()
# hilo_voz.start()

# Esperar a que todos los hilos terminen
hilo_camara.join()
hilo_serial.join()
# hilo_voz.join()

print("Los hilos han terminado su ejecución.")