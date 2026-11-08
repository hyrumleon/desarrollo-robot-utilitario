import serial
import time

puerto = '/dev/ttyUSB0'
#puerto    = '/dev/ttyACM0'

baud_rate = 115200
#baud_rate = 9600

 
def conectar_puerto(puerto, baud_rate):
    while True:
        try:
            ser = serial.Serial(puerto, baud_rate, timeout=1)
            print(f"Conectado al puerto {puerto}")
            return ser
        except serial.SerialException as e:
            print(f"Error al conectar al puerto {puerto}. Reintentando en 3 segundos...")
            time.sleep(3)

def leer_datos(ser):
    while True:
        try:
            if ser.in_waiting > 0:
                linea = ser.readline().decode('utf-8', errors='replace').strip()
                print(linea)
        except (serial.SerialException, OSError) as e:
            print(f"Error en la conexion: {e}. Intentando reconectar...")
            ser.close()
            return False
        except KeyboardInterrupt:
            print("\nLectura interrumpida por el usuario.")
            ser.close()
            exit(0)

def main():
    while True:
        try:
            ser = conectar_puerto(puerto, baud_rate)
            if not leer_datos(ser):
                time.sleep(2)
        except Exception as e:
            print(f"Error inesperado: {e}. Reiniciando...")
            time.sleep(2)

if __name__ == "__main__":
    main()
