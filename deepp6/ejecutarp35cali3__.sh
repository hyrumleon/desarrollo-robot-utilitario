#!/bin/bash

# Configurar la variable DISPLAY para que el script acceda al entorno grico
export DISPLAY=:0



#export XAUTHORITY=/home/pi/.Xauthority
#export PULSE_SERVER=localhost
#export ALSA_CONFIG_PATH=/etc/alsa/pulse/alsa.conf


# Registrar inicio del script en el archivo de log
echo "Inicio del script" >> /home/pi/cron_debug.log

# Cerrar orca si está corriendo
pkill orca >> /home/pi/cron_debug.log 2>&1

# Ir a la carpeta correcta
cd /home/pi/Desktop/HYRUM/arucooo >> /home/pi/cron_debug.log 2>&1

# Activar el entorno virtual
source /home/pi/Desktop/HYRUM/arucooo/env/bin/activate >> /home/pi/cron_debug.log 2>&1

# Verificar si el entorno virtual se activó correctamente
echo "Entorno virtual activado: $VIRTUAL_ENV" >> /home/pi/cron_debug.log

# Enlazar el dispositivo Bluetooth
sudo rfcomm bind /dev/rfcomm0 0C:B8:15:CB:78:7E >> /home/pi/cron_debug.log 2>&1

# Ir al directorio correcto para el script Python
cd /home/pi/Desktop/HYRUM/arucooo/deepp >> /home/pi/cron_debug.log 2>&1

# Ejecutar el script Python
echo "Ejecutando el script p35_cali3.py..." >> /home/pi/cron_debug.log
python3 /home/pi/Desktop/HYRUM/arucooo/deepp/p35_cali3.py >> /home/pi/cron_debug.log 2>&1
echo "Script ejecutado con estado: $?" >> /home/pi/cron_debug.log
