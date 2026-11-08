import cv2
import numpy as np
import face_recognition as fr
import os
import random
import time



#from picamera2 import Picamera2



import time

# Ruta de la base de datos de rostros
path = r'C:\Users\leonl\Downloads\arauco2\DEEPp5\deepp6\know_faces'

# Función para cargar imágenes y nombres de la base de datos
def cargar_base_datos(path):
    images = []
    classes = []
    lista = os.listdir(path)
    for lis in lista:
        imgdb = cv2.imread(f'{path}/{lis}')
        images.append(imgdb)
        classes.append(os.path.splitext(lis)[0])
    return images, classes

# Función para codificar los rostros
def codrostros(images):
    listacod = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(img)
        if not cod:
            print("Advertencia: No se detectó rostro en una de las imágenes de la base de datos.")
            continue
        listacod.append(cod[0])
    return listacod

# Función para agregar un nuevo rostro a la base de datos
def agregar_rostro(nuevo_rostro, nombre, images, classes, rostroscod, path):
    nuevo_rostro_rgb = cv2.cvtColor(nuevo_rostro, cv2.COLOR_BGR2RGB)
    codificaciones = fr.face_encodings(nuevo_rostro_rgb)
    if not codificaciones:
        print("Error: No se pudo detectar un rostro en la imagen proporcionada.")
        return images, classes, rostroscod

    # Guardar imagen del nuevo rostro
    cv2.imwrite(f'{path}/{nombre}.jpg', nuevo_rostro)
    images.append(nuevo_rostro)
    classes.append(nombre)
    rostroscod.append(codificaciones[0])
    print(f"Nuevo rostro agregado: {nombre}")
    return images, classes, rostroscod

# Función principal para detección de rostros
def procesar_frame(frame, images, rostroscod, classes, start_time, path, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    rostro_detectado = False

    for (x, y, w, h) in faces:
        rostro_nuevo = frame[y:y+h, x:x+w]
        rostro_rgb = cv2.cvtColor(rostro_nuevo, cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(rostro_rgb)

        if cod:
            rostro_detectado = True
            comparacion = fr.compare_faces(rostroscod, cod[0])
            simi = fr.face_distance(rostroscod, cod[0])
            min_idx = np.argmin(simi)

            if comparacion[min_idx]:
                nombre = classes[min_idx].upper()
                r, g, b = [random.randrange(0, 255, 50) for _ in range(3)]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (r, g, b), 3)
                cv2.rectangle(frame, (x, y-35), (x+w, y), (r, g, b), cv2.FILLED)
                cv2.putText(frame, nombre, (x+6, y-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                print(f"Rostro detectado: {nombre}")
            else:
                if start_time is None:
                    print("Rostro desconocido detectado. Iniciando contador...")
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 2.5:
                        print("Tiempo alcanzado. Agregando nuevo rostro...")
                        nuevo_nombre = f"rostro_{len(classes) + 1}"
                        images, classes, rostroscod = agregar_rostro(rostro_nuevo, nuevo_nombre, images, classes, rostroscod, path)
                        start_time = None
    if not rostro_detectado:
        start_time = None

    return frame, start_time, images, rostroscod, classes



def procesar_frame2(frame, images, rostroscod, classes, start_time, path, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    rostro_detectado = False
    nombres_detectados = []  # Lista para almacenar los nombres detectados

    for (x, y, w, h) in faces:
        rostro_nuevo = frame[y:y+h, x:x+w]
        rostro_rgb = cv2.cvtColor(rostro_nuevo, cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(rostro_rgb)

        if cod:
            rostro_detectado = True
            comparacion = fr.compare_faces(rostroscod, cod[0])
            simi = fr.face_distance(rostroscod, cod[0])
            min_idx = np.argmin(simi)

            if comparacion[min_idx]:
                nombre = classes[min_idx].upper()
                nombres_detectados.append(nombre)  # adir nombre a la lista
                r, g, b = [random.randrange(0, 255, 50) for _ in range(3)]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (r, g, b), 3)
                cv2.rectangle(frame, (x, y-35), (x+w, y), (r, g, b), cv2.FILLED)
                cv2.putText(frame, nombre, (x+6, y-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                print(f"Rostro detectado: {nombre}")
            else:
                if start_time is None:
                    print("Rostro desconocido detectado. Iniciando contador...")
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 2.5:
                        print("Tiempo alcanzado. Agregando nuevo rostro...")
                        nuevo_nombre = f"rostro_{len(classes) + 1}"
                        images, classes, rostroscod = agregar_rostro(rostro_nuevo, nuevo_nombre, images, classes, rostroscod, path)
                        start_time = None
    if not rostro_detectado:
        start_time = None

    return frame, start_time, images, rostroscod, classes, nombres_detectados


if __name__ == "__main__":
    # Cargar base de datos inicial
    images, classes = cargar_base_datos(path)
    rostroscod = codrostros(images)


    picam2 = Picamera2()
    #picam2.preview_configuration.main.format = "RGB888"  # Establecer formato de color natural
    picam2.configure(picam2.create_video_configuration())  # Cambiar a configu de video
    
    print("Inicianmara")
    picam2.start()
    time.sleep(2)
    
    # Cargar el clasificador Haar
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    start_time = None

    while True:
        
        image = picam2.capture_array()
        
        frame = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        

        frame, start_time, images, rostroscod, classes , nombres= procesar_frame2(frame, images, rostroscod, classes, start_time, path, face_cascade)
        if nombres:
            print(nombres)
        cv2.imshow("Reconocimiento Facial", frame)

        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            break

    # Liberar recursos
    
    picam2.stop()
    
    cv2.destroyAllWindows()
