pkill orca
cd /home/pi/Desktop/HYRUM/arucooo
source env/bin/activate
sudo rfcomm bind /dev/rfcomm0 0C:B8:15:CB:78:7E
cd /home/pi/Desktop/HYRUM/arucooo/deepp
python3 p35_cali3.py
#!/bin/bash
#!/bin/bash
#export DISPLAY=:0
#set -x

## Redirigir la salida estándar y los errores a un archivo de log
#LOGFILE="/home/pi/Desktop/ejecutarp10_log.txt"
#exec > >(tee -a $LOGFILE) 2>&1
#lxterminal -e "
    #pkill orca;
    #cd /home/pi/Desktop/HYRUM/arucooo;
    #source env/bin/activate;
    #sudo rfcomm bind /dev/rfcomm0 0C:B8:15:CB:78:7E;
    #cd /home/pi/Desktop/HYRUM/arucooo/deepp;
    #python3 p35_cali3.py >> $LOGFILE 2>$1;
    #echo 'Presiona Enter para cerrar...';
    #read
#" > /home/pi/Desktop/terminal_output.log 2>&1


