import RPi.GPIO as GPIO
import time

BUTTON_GPIO = 24
LED_GPIO = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_GPIO, GPIO.OUT)

def controlar_led():
    while True:
        if GPIO.input(BUTTON_GPIO) == GPIO.HIGH:
            GPIO.output(LED_GPIO, True)
            print("LED encendido.")
        else:
            GPIO.output(LED_GPIO, False)
            print("LED apagado.")
        
        time.sleep(1)

controlar_led()
