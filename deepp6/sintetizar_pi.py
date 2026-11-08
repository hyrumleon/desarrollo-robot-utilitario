import pyttsx3
import time

def hablar(texto, velocidad=100):  # Velocidad ajustada a 100
    # Inicializar el motor de pyttsx3
    motor = pyttsx3.init()

    # Buscar y seleccionar la voz de "Spanish (Latin America)"
    voces = motor.getProperty('voices')
    voz_encontrada = False
    for voz in voces:
        if voz.id == "Spanish (Latin America)":
            motor.setProperty('voice', voz.id)
            voz_encontrada = True
            print("Voz 'Spanish (Latin America)' seleccionada correctamente.")
            break
    
    if not voz_encontrada:
        print("Voz 'Spanish (Latin America)' no encontrada. Usando voz por defecto.")
    
    # Configurar la velocidad y el volumen
    motor.setProperty('rate', velocidad)
    motor.setProperty('volume', 1)
    print(f"Configuracion: velocidad={motor.getProperty('rate')}, volumen={motor.getProperty('volume')}")
    
    # Pronunciar el texto
    print(f"Pronunciando texto: {texto}")
    motor.say(texto)
    motor.runAndWait()  # Espera a que el motor termine de hablar antes de continuar

    # Guardar el texto en un archivo de audio
    #time.sleep(1.5)
    # print("Guardando el archivo de audio...")
    # motor.save_to_file(texto, 'test.mp3')
    # motor.runAndWait()  # Asegura que el archivo se guarde correctamente

    print("Finalizo la reproduccion y guardado del texto.")


if __name__ == "__main__":
    # Definir una lista de tareas
    tareas = ["limpiar la casa", "hacer la compra", "estudiar para el examen", "preparar la cena"]
    tarea = 1  # Por ejemplo, seleccionar la segunda tarea en la list
    
    # Preguntar al usuario si desea ejecutar la tarea
    hablar(str(f"Deseas ejecutar la tarea: {tareas[tarea]}"), velocidad=70)
