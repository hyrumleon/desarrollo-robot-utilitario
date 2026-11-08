import serial
import time

puerto_1 = '/dev/ttyUSB0'
puerto_2 = '/dev/rfcomm0'
baud_rate = 115200

def conectar_puerto(puerto, baud_rate):
    while True:
        try:
            ser = serial.Serial(puerto, baud_rate, timeout=1)
            print(f"Conectado al puerto {puerto}")
            return ser
        except serial.SerialException as e:
            print(f"Error al conectar al puerto {puerto}: {e}. Intentando nuevamente...")
            time.sleep(2)

def leer_datos(ser_1, ser_2):
    while True:
        try:
            # Leer datos de puerto 1
            if ser_1.in_waiting > 0:
                linea_1 = ser_1.readline().decode('utf-8', errors='replace').strip()
                print(f"Puerto 1: {linea_1}")

            # Leer datos de puerto 2
            if ser_2.in_waiting > 0:
                linea_2 = ser_2.readline().decode('utf-8', errors='replace').strip()
                print(f"Puerto 2: {linea_2}")

        except (serial.SerialException, OSError) as e:
            print(f"Error en la conen: {e}. Cerrando conexiones y reiniciando...")
            ser_1.close()
            ser_2.close()
            return False
        except KeyboardInterrupt:
            print("\nLectura interrumpida por el usuario.")
            ser_1.close()
            ser_2.close()
            exit(0)

def main():
    while True:
        try:
            # Conectar a los puertos por separado
            print("Conectando al puerto 1...")
            ser_1 = conectar_puerto(puerto_1, baud_rate)

            print("Conectando al puerto 2...")
            ser_2 = conectar_puerto(puerto_2, baud_rate)

            # Leer datos de ambos puertos
            if not leer_datos(ser_1, ser_2):
                time.sleep(2)  # Esperamos antes de intentar nuevamente
        except Exception as e:
            print(f"Error inesperado: {e}. Reiniciando...")
            time.sleep(2)

if __name__ == "__main__":
    main()
