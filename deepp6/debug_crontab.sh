#!/bin/bash
echo "=== Fecha y hora ===" > /home/pi/crontab_debug.log
date >> /home/pi/crontab_debug.log

echo "=== Usuario actual ===" >> /home/pi/crontab_debug.log
whoami >> /home/pi/crontab_debug.log

echo "=== Grupos del usuario ===" >> /home/pi/crontab_debug.log
groups >> /home/pi/crontab_debug.log

echo "=== Entorno ===" >> /home/pi/crontab_debug.log
env >> /home/pi/crontab_debug.log

echo "=== Permisos de /dev/video2 ===" >> /home/pi/crontab_debug.log
ls -l /dev/video2 >> /home/pi/crontab_debug.log

echo "=== Dispositivos de audio ===" >> /home/pi/crontab_debug.log
arecord -l >> /home/pi/crontab_debug.log

echo "=== Probar conexión a tarjeta 3 ===" >> /home/pi/crontab_debug.log
arecord -D hw:3,0 -f cd -d 2 /dev/null 2>> /home/pi/crontab_debug.log
if [ $? -eq 0 ]; then
    echo "Conexión a tarjeta 3 exitosa" >> /home/pi/crontab_debug.log
else
    echo "Error al conectar con tarjeta 3" >> /home/pi/crontab_debug.log
fi

echo "=== Permisos en /dev/snd ===" >> /home/pi/crontab_debug.log
ls -l /dev/snd >> /home/pi/crontab_debug.log