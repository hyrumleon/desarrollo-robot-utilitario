#!/bin/bash
#set +m

echo "La hora actual es: $(date '+%H:%M:%S')" >> /home/pi/crontab_debug.log 2>&1
pkill orca

export DISPLAY=:0
export PATH=$PATH:/usr/local/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=/usr/lib:/lib
export ALSA_CARD=Device
export AUDIODEV=hw:3,0


pkill orca

pkill orca >> /home/pi/crontab_debug.log 2>&1
cd /home/pi/Desktop/HYRUM/arucooo || exit
source env/bin/activate
sudo rfcomm bind /dev/rfcomm0 0C:B8:15:CB:78:7E
cd /home/pi/Desktop/HYRUM/arucooo/deepp || exit
ls /home/pi/Desktop/HYRUM/arucooo/deepp/ >> /home/pi/crontab_debug.log 2>&1
python3 p_cam2.py >> /home/pi/crontab_debug.log 2>&1