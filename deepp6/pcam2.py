import cv2

# Selecciona la 
camera_index = 0 # Cambia a 1 si quieres usar la seg

cap = cv2.VideoCapture(camera_index)

if cap.isOpened():
    print(f"mara {camera_index}. Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el cuadro.")
            break
        cv2.imshow(f"mara {camera_index}", frame)

        # Presiona 'q' para cerrar la ventana
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print(f"No se pudo abrir lmara {camera_index}.")
