#!/bin/bash
#Script to submit abaqus jobs via python script
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16g
#SBATCH --time=1:00:00


#!/bin/bash
filename=./ArealDensity.txt
filesize1=$(stat -c%s "$filename")
echo "Size of $filename = $filesize1 bytes."



#below use Linux commands, which will run on compute node
cd ${SLURM_SUBMIT_DIR}
#load modules and export to paths so can call the TexGen functions
module load GCCcore/6.3.0
module load binutils/2.27-GCCcore-6.3.0
export PATH=/gpfs01/home/emxghs/bin:$PATH
export LD_LIBRARY_PATH=/gpfs01/home/emxghs/Python-2.7.16/Lib/site-packages/TexGen:$LD_LIBRARY_PATH

cd /gpfs01/home/emxghs/IAA3DWeaveProject
/gpfs01/home/emxghs/bin/python /gpfs01/home/emxghs/IAA3DWeaveProject/parameterisedTextile.py $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} ${21} ${22} ${23}
#Read the output to check if weave violates feasibility rules and should not be run
#to do: check whether .inp file has been generated 

filename=./ArealDensity.txt
filesize2=$(stat -c%s "$filename")
echo "Size of $filename = $filesize2 bytes."
while [[ filesize2 < filesize1 ]]
do 
	sleep 1
	filesize2=$(stat -c %s "$filename")
	echo "Size of $filename = $filesize2 bytes."
done

wait
wait
