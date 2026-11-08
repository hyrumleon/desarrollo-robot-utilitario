import pyttsx3 
import time

def hablar2(texto, velocidad=100):
    motor = pyttsx3.init()
    motor.setProperty('voice', 'es-419')
    motor.setProperty('rate', velocidad)
    motor.setProperty('volume', 1)
    time.sleep(0.5)
    print(f"Configuracion: velocidad={motor.getProperty('rate')}, volumen={motor.getProperty('volume')}")
    print(f"Pronunciando texto: {texto}")
    print(f"Velocidad antes de pronunciar: {motor.getProperty('rate')}")
    texto = str(texto)
    motor.say(texto)
    motor.runAndWait()
    motor.stop()
    del motor
    print("Finalizo la reproduccion.")

def main():

    tareas = ["limpiar la casa", "hacer la compra", "estudiar para el examen", "preparar la cena"]
    tarea = 1
    texto = str(f"Deseas ejecutar la tarea: {tareas[tarea]}")
    hablar2(texto, velocidad=70)
    