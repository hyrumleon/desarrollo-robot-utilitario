import subprocess
import os
import sys

# Ruta completa del archivo .sh
sh_file = "/home/pi/Desktop/HYRUM/arucooo/deepp/ejecutarp10__.sh"

def ejecutar_sh():
    # Asegurarse de que el archivo tiene permisos de ejecucn
    try:
        os.chmod(sh_file, 0o755)  # Da permisos de ejecucn
        print(f"Permisos otorgados a: {sh_file}")
    except Exception as e:
        print(f"Error al otorgar permisos: {e}")
        sys.exit(1)  # Salir con error

    # Ejecutar el archivo .sh
    try:
        subprocess.run(["/bin/bash", sh_file], check=True)
        print("Archivo .sh ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el archivo .sh: {e}")
        sys.exit(1)  # Salir con error

# Ejecutar la funcin principal
if __name__ == "__main__":
    ejecutar_sh()
    # Terminar el script de Python
    sys.exit(0)
