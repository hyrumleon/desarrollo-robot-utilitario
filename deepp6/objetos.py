import cv2

def process_frame(frame, net, classes, confidence_threshold=0.45):
    """
    Procesa un cuadro de video para detectar objetos utilizando un modelo DNN.

    Args:
        frame (numpy.ndarray): Cuadro de video capturado.
        net (cv2.dnn_Net): Red neuronal cargada para detección.
        classes (dict): Diccionario de clases con sus nombres.
        confidence_threshold (float): Umbral mínimo de confianza para detecciones.

    Returns:
        list: Lista de objetos detectados con sus características.
    """
    original_height, original_width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), (127.5, 127.5, 127.5))
    net.setInput(blob)
    detections = net.forward()

    detected_objects = []
    for detection in detections[0, 0]:
        if detection[2] > confidence_threshold:
            label = classes.get(int(detection[1]), "Unknown")
            box = detection[3:7] * [original_width, original_height, original_width, original_height]
            x_start, y_start, x_end, y_end = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            x_center = (x_start + x_end) // 2
            y_center = (y_start + y_end) // 2

            detected_objects.append({
                "label": label,
                "confidence": detection[2],
                "box": (x_start, y_start, x_end, y_end),
                "center": (x_center, y_center)
            })

    return detected_objects

if __name__ == "__main__":
    
    # ----------- USO DE LA FUNCIÓN -----------

    # Leer modelo y configuraciones
    prototxt = "MobileNetSSD_deploy.prototxt.txt"
    model = "MobileNetSSD_deploy.caffemodel"
    classes = {
        0: "background", 1: "aeroplane", 2: "bicycle",
        3: "bird", 4: "boat", 5: "bottle", 6: "bus",
        7: "car", 8: "cat", 9: "chair", 10: "cow",
        11: "diningtable", 12: "dog", 13: "horse",
        14: "motorbike", 15: "person", 16: "pottedplant",
        17: "sheep", 18: "sofa", 19: "train", 20: "tvmonitor"
    }
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # Capturar video desde la cámara
    cap = cv2.VideoCapture('/dev/video0')
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el cuadro.")
            break

        # Procesar el cuadro
        detections = process_frame(frame, net, classes)

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
                print(f"Ancho en píxeles: {width}")
                
                # Definir los puntos dados
                x2, y2, x1, y1= 66, .5, 29, 1
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

        # Mostrar el cuadro
        cv2.imshow("Detección en tiempo real", frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

