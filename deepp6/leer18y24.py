import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.setup(24, GPIO.IN)

try:
    while True:
        input18 = GPIO.input(18)
        input24 = GPIO.input(24)

        print(f"Pin 18: {'Alto' if input18 else 'Bajo'}")
        print(f"Pin 24: {'Alto' if input24 else 'Bajo'}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
finally:
    GPIO.cleanup()
