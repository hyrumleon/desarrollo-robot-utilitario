import RPi.GPIO as GPIO
import time

# Configurar los pines
GPIO.setmode(GPIO.BCM)

# Entradas (botones)
GPIO.setup(18, GPIO.IN)
GPIO.setup(24, GPIO.IN)

# Salidas (LEDs)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

try:
    while True:
        input18 = GPIO.input(18)
        input24 = GPIO.input(24)

        # Imprimir el estado de los botones
        print(f"Pin 18: {'Alto' if input18 else 'Bajo'}")
        print(f"Pin 24: {'Alto' if input24 else 'Bajo'}")

        # Controlar los LEDs basados en el estado de los botones
        GPIO.output(15, input18)  # Enciende el LED en el pin 15 si el
        GPIO.output(23, input24)  # Enciende el LED en el pin 23 si

        time.sleep(1)

except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
finally:
    GPIO.cleanup()
