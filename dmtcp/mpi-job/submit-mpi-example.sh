#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --time=00:15:00
#SBATCH --partition=debug
#SBATCH -J exercise3-mpi
#SBATCH --output=dmtcp_mpi_%A.out
#SBATCH --error=dmtcp_mpi_%A.err

module load dmtcp/2.6.0
module load gcc/10.2
module avail mpi/mvapich2-2.3.5_gcc_10.2_slurm22


RESTARTSCRIPT="dmtcp_restart_script.sh"
export DMTCP_QUIET=0

runcmd="./mpi-example"
tint=30

echo "Start coordinator"
date
eval "dmtcp_coordinator --daemon --coord-logfile dmtcp_log.txt --exit-after-ckpt --exit-on-last -i "$tint" --port-file cport.txt -p 0"
sleep 2
cport=$(<cport.txt)
echo $cport
h=`hostname`
echo $h

export DMTCP_COORD_HOST=$h
export DMTCP_COORD_PORT=$cport

HOSTFILE=hostfile
echo "SLURM_JOB_NODELIST" | scontrol show hostname > $HOSTFILE

if [ -f "$RESTARTSCRIPT" ] 
then
    echo "Resume the application"
    ./dmtcp_restart_script.sh -h $DMTCP_COORD_HOST -p $DMTCP_COORD_PORT
else
    echo "Start the application"
    srun --mpi=pmix --export=ALL dmtcp_launch --no-gzip --rm $runcmd
fi

echo "Stopped program execution"
date
sleep 2