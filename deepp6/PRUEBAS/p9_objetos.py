import os

import sys

#os.system(r'env\Scripts\activate && cd C:\Users\leonl\Downloads\arauco2\deepp\PRUEBAS && python p9_objetos.py')
os.system(r'env\Scripts\activate && cd C:\Users\leonl\Downloads\arauco2\deepp && python p10__.py')

#sys.path.append(r'C:\Users\leonl\Downloads\arauco2\deepp')
import threading# Función para manejar la captura de la cámara


def actualizar_variables(variables):
    global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA
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


def captura_camara():
    
    global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA , gesto
    
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
    from mano import process_hand_frame
    # Inicializar MediaPipe para detección de manos
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands()

##############################################################################################################
    # Ruta de la base de datos de rostros
    path = r'C:\Users\leonl\Downloads\arauco2\deepp\know_faces'

    from rostross import procesar_frame , cargar_base_datos , codrostros

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

    low_res_size = (40, 30)  # Tamaño reducido para el procesamiento
    # Configuración de DepthAnything
    depth_anything = DepthAnythingInference(model_path='depth_anything/models/depth_anything_vits14.onnx', color=True)
    line_number = 15  # Ajustado para la resolución reducida

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



    # # Matriz de la cámara (K)
    # K = np.array([[1701.46226, 0.0, 468.10957],
    #             [0.0, 1690.89815, 369.38506],
    #             [0.0, 0.0, 1.0]], dtype=float)

    # # Coeficientes de distorsión (D)
    # D = np.array([0.07543864, 0.84724384, 0.01396338, -0.03902927, -1.23286897], dtype=float)


    # Matriz intrínseca y coeficientes de distorsión calibrados
    K = np.array([[724.01480023, 0, 326.76948321],
                [0, 718.8967463, 320.74633705],
                [0, 0, 1]], dtype=float)
    D = np.array([-0.2, 0.1, 0, 0, 0])

    # Datos para la relación l
    # Ejemplo de uso con la captura de video
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Corrección de distorsión
        frame_undistorted = cv2.undistort(frame, K, D)

        # Conversión de BGR a RGB para Mediapipe
        frame_rgb = cv2.cvtColor(frame_undistorted, cv2.COLOR_BGR2RGB)
        
        gray = cv2.cvtColor(frame ,cv2.COLOR_BGR2GRAY)


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
        # Llamar a la función de detección y obtener los resultados
        result = detect_marker_distance_and_angle(gray)


        if result:
            displacement_x_24, displacement_y_24, distance_24, displacement_x_34, displacement_y_34, distance_34, angle_A_degrees = result
            print(f"Displacement 24: {displacement_x_24:.2f}, {displacement_y_24:.2f}, Distance 24: {distance_24:.2f}")
            print(f"Displacement 34: {displacement_x_34:.2f}, {displacement_y_34:.2f}, Distance 34: {distance_34:.2f}")

            print(f"Angle between markers: {angle_A_degrees:.2f} degrees")
        else:
            print("No se detectaron los marcadores 24 y 34.")
            
        
        
        # Ejemplo de uso con los parámetros
        a9 = 3
        a7 = 2.8
        a3 = 3.3


        coordenada_X, coordenada_Y,angulo_Z_grados = realizar_calculos(a9 = a9, a7 = a7,  a3 = a3, t7 = 20  , a1 = 3.3, a2 = 3, )

        print("\nResultado final:")
        print(f"Coordenada X: {coordenada_X}")
        print(f"Coordenada Y: {coordenada_Y}")
        print(f"Ángulo en Z: {angulo_Z_grados}")
        
        
        
        frame, start_time, images, rostroscod, classes = procesar_frame(frame, images, rostroscod, classes, start_time, path, face_cascade)
    
        
        gesto = ""
        # Procesar la imagen para obtener la posición y distancia
        center_x, center_y, gesto, real_depth = process_hand_frame(mp_hands, mp_drawing, hands, frame_rgb)
        
        # Asignar valores solo si no son None
        if center_x is not None:
            dx = center_x
        if center_y is not None:
            dy = center_y
            
        if real_depth is not None:
            dz = real_depth   

        if center_x is not None and center_y is not None:
            # Mostrar el resultado en el frame
            cv2.putText(frame_undistorted, f"Centro: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame_undistorted, f"Gesto: {gesto}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame_undistorted, f"Distancia Real: {real_depth:.2f} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
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
                # Obtener las coordenadas de la caja delimitadora
                x_start, y_start, x_end, y_end = obj['box']

                # Calcular el ancho en píxeles
                width = x_end - x_start
                print(f"Ancho en píxeles: {width}")
                
                # Definir los puntos dados
                x2, y2, x1, y1= 30, .7, 60, 0.2
                x = width
                




                # Calcular y en una sola línea
                z_car = ((y2 - y1) / (x2 - x1)) * (x - x1) + y1

                # Mostrar el resultado
                
                print(f"Cuando x = {x}, y = {z_car}")

                
                

            

            
                
            

            # Dibujar en el cuadro
            x_start, y_start, x_end, y_end = obj['box']
            cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
            cv2.putText(frame, f"{obj['label']} ({obj['confidence'] * 100:.2f}%)",
                        (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Mostrar el frame
        cv2.imshow("Frame", frame_undistorted)
        cv2.imshow("Reconocimiento Facial", frame)








        # Salir con la tecla ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break
        

    cap.release()
    cv2.destroyAllWindows()





# Función para manejar la lectura/escritura en el puerto serial
def manejar_serial():
    global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA , gesto
    #M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA = [0] * 13  # Inicializar en 
    import serial
    import time
    import re
    import matplotlib.pyplot as plt
    
    #sys.path.append(r'C:\Users\leonl\Downloads\arauco2\deepp')
    print(dz)
    from g2f import  agregar_a_lista, enviar_mensaje , leer_datos, actualizar_grafica
    
    
    from pxy12T import manejar_busqueda
#####################################################################################################
    def conectar_puerto(puerto, baudrate, timeout=5):
        """Intenta conectar al puerto serial dentro de un tiempo límite."""
        start_time = time.time()
        while True:
            try:
                print(f"Intentando conectar al puerto {puerto}...")
                conexion = serial.Serial(puerto, baudrate, timeout=1)
                print("¡Conexión establecida!")
                return conexion
            except serial.SerialException as e:
                elapsed_time = time.time() - start_time
                print(f"No se pudo conectar: {e}")
                if elapsed_time > timeout:
                    print("Tiempo de espera agotado. Reiniciando el programa...")
                    
            time.sleep(1)  # Espera un segundo antes de intentar de nuevo
    # Configuración del puerto y la velocidad de transmisión
    port = 'COM16'
    baud_rate = 9600
    esp32 = conectar_puerto(port, baud_rate)

    # Intervalo de tiempo en segundos entre envíos
    intervalo_envio = .18
    ultimo_envio = time.time()

    # Contador de mensajes enviados
    contador_mensajes = 0

    # Inicializamos la lista que se utilizará para almacenar los datos
    lista_datos = []
    trayectoria = []

    # Inicializar figura para graficar
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("XA")
    ax.set_ylabel("YA")

    # Bucle principal
    try:
        while True:
            
            # Enviar datos en intervalos
            if time.time() - ultimo_envio >= intervalo_envio:
                contador_mensajes, lista_datos = enviar_mensaje(esp32, contador_mensajes, lista_datos)
                ultimo_envio = time.time()

            # Agregar elementos a la lista
            #lista_datos = agregar_a_lista("dx2", lista_datos)
            lista_datos = agregar_a_lista("AS-0.0", lista_datos)
            lista_datos = agregar_a_lista("BS0.0", lista_datos)
            lista_datos = agregar_a_lista(f"XD0.0", lista_datos)
            lista_datos = agregar_a_lista(f"YD0.0", lista_datos)
            lista_datos = agregar_a_lista("CT0", lista_datos)
            
            
            if gesto is not None and (
                "Mano en forma de garra: Cambiar a modo de espera o ahorro de energía" in gesto or 
                "Mano en forma de cuerno: Cambiar a modo de espera o ahorro de energía" in gesto) and dx is not None and dz is not None:
                
                lista_datos = agregar_a_lista(f"dx{dx:.2f}", lista_datos)
                lista_datos = agregar_a_lista(f"dz{dz/100:.2f}", lista_datos)
                lista_datos = agregar_a_lista("CS1", lista_datos)

            else:
                lista_datos = agregar_a_lista("CS0", lista_datos)

            # Leer datos recibidos  
            variables = leer_datos(esp32)
            if variables:
                actualizar_variables(variables)
                print(f"Datos actualizados: M={M}, A={A}, CA={CA}, AM={AM}, dz={dz}, dx={dx}, dy={dy}, g={g}, XA={XA}, YA={YA}, XB={XB}, YB={YB}, PA={PA}")
                trayectoria = actualizar_grafica(ax,trayectoria, XA, YA)
                
                
            
                xt , yt , CT  = 1.6, 0, 1
                
                if XA is not None and YA is not None:
                    XB, YB = manejar_busqueda( XA, -YA , xt, -yt, bool(CT))
                    print("Coordenadas 1:", XB)
                    print("Coordenadas 2:", YB)








    except KeyboardInterrupt:
        print("Finalizando programa...")
        plt.close()
        esp32.close()
        


# Función para manejar comandos de voz
def manejar_voz():
    
        
    from escuchar import escuchar_comando0 , confirmar_tarea, procesar_comando
    
    from sintetizar_pi import hablar
    tareas = {
        "encender_luz": "Encendiendo la luz...",
        "apagar_luz": "Apagando la luz...",
        "reproducir_musica": "Reproduciendo música...",
        "detener_musica": "Deteniendo la música...",
        "seguir_mano": "Siguiendo la mano...",
        "detener_seguir_mano": "Deteniendo la tarea de seguir mano...",
        "seguir_objeto": "Siguiendo el objeto...",
        "detener_seguir_objeto": "Deteniendo la tarea de seguir objeto...",
        "monitorear_temperatura": "Monitoreando la temperatura...",
        "detener_monitorear_temperatura": "Deteniendo la tarea de monitoreo de temperatura..."
    }



    # Palabras clave de acciones (con sinónimos)
    palabras_clave = {
        "encender_luz": {"verbo": ["encender", "prender"], "sustantivo": ["luz", "foco"]},
        "apagar_luz": {"verbo": ["apagar"], "sustantivo": ["luz", "foco"]},
        "reproducir_musica": {"verbo": ["reproducir", "tocar"], "sustantivo": ["música", "canción"]},
        "detener_musica": {"verbo": ["detener", "parar", "quita"], "sustantivo": ["música", "canción"]},
        "seguir_mano": {"verbo": ["seguir"], "sustantivo": ["mano"]},
        "detener_seguir_mano": {"verbo": ["detener", "parar", "dejar"], "sustantivo": ["seguir", "mano"]},
        "seguir_objeto": {"verbo": ["seguir"], "sustantivo": ["objeto"]},
        "detener_seguir_objeto": {"verbo": ["detener", "parar"], "sustantivo": ["seguir", "objeto"]},
        "monitorear_temperatura": {"verbo": ["monitorear", "controlar"], "sustantivo": ["temperatura", "calor"]},
        "detener_monitorear_temperatura": {"verbo": ["detener", "parar"], "sustantivo": ["monitorear", "temperatura"]}
    }






    # Lista de palabras que indican negación
    palabras_negacion = ["evitar", "cancelar", "dejar", "parar", "no"]

    # Lista de palabras que indican "alto" y sinónimos
    palabras_alto = ["alto", "detente", "parar", "detener", "alto ahí"]


    # Lista de palabras que indican "sí" y "no"
    palabras_si = ["sí", "si", "claro", "por supuesto", "afirmativo"]
    palabras_no = ["no", "negativo", "para nada", "nada"]

    



    while True:
        # Implementar la lógica de reconocimiento de voz aquí
        print("Procesando comandos de voz...")
        
        hablar("Escuchando" , velocidad = 70)
        comando = escuchar_comando0()
        if comando:
            tarea = procesar_comando(comando, palabras_clave , palabras_alto )
            
            
            
            
            
            if tarea == "alto":
                alto_por_comando = True
                
                seguir_mano = False
                seguir_objeto = False
                monitorear_temp = False
                print("Bandera 'Alto' activada. Todas las otras tareas detenidas.")
                #return  # Salir de la función después de activar la bandera "alto"

            if tarea in tareas:
                
                
                
                print(f"¿Deseas ejecutar la tarea: '{tareas[tarea]}'? (Di 'sí' o 'no')")
                hablar(f"¿Deseas ejecutar la tarea: '{tareas[tarea]}'?", velocidad = 70)
                respuesta = escuchar_comando0()  # Esperar la respuesta del usuario
                
                if confirmar_tarea(respuesta, palabras_si , palabras_no):  # Pregunta al usuario si desea ejecutar la tarea
                    print(tareas[tarea])
                else:
                    print("Tarea cancelada por el usuario.")
            elif tarea == "no_tarea":
                print("No se ejecutará ninguna tarea debido a la negación.")
            else:
                
                
                print("No se pudo identificar la tarea.")
            
            

# Declarar todas las variables globales
global M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA, gesto
M, A, CA, AM, dz, dx, dy, g, XA, YA, XB, YB, PA = [0] * 13  # Inicializar en 0

dz = 50


dx = 500
gesto = ""



# Crear los hilos
hilo_camara = threading.Thread(target=captura_camara)
hilo_serial = threading.Thread(target=manejar_serial)
hilo_voz = threading.Thread(target=manejar_voz)

# Iniciar los hilos
hilo_camara.start()
hilo_serial.start()
hilo_voz.start()

# Esperar a que todos los hilos terminen
hilo_camara.join()
hilo_serial.join()
hilo_voz.join()

print("Los hilos han terminado su ejecución.")