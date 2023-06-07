#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:05:00
#SBATCH --partition=debug
#SBATCH --job-name=exercise3-serial
#SBATCH --output=dmtcp_serial_%A.out
#restart script

module load dmtcp/2.6.0

RESTARTSCRIPT="dmtcp_restart_script.sh"
export DMTCP_QUIET=2

runcmd="./serial"
tint=30

echo "Start coordinator"
date
eval "dmtcp_coordinator --daemon --coord-logfile dmtcp_log.txt --exit-after-ckpt --exit-on-last -i "$tint" --port-file cport.txt -p 0"
##Uncomment the line below and comment the line above to avoid stopping the job after ckpting
##eval "dmtcp_coordinator --daemon --coord-logfile dmtcp_log.txt --exit-on-last -i "$tint" --port-file cport.txt -p 0"
sleep 2
cport=$(<cport.txt)
echo "$cport"
h=`hostname`
echo $h

if [ -f "$RESTARTSCRIPT" ]
then
    echo "Resume the application"
    CMD="dmtcp_restart -p "$cport" -i "$tint" ckpt*.dmtcp"
    echo $CMD
    eval $CMD
else
    echo "Start the application"
    CMD="dmtcp_launch --rm --no-gzip -h localhost -p "$cport" "$runcmd
    echo $CMD
    eval $CMD
fi

echo "Stopped program execution"
date