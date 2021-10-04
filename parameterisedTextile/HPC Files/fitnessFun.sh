#!/bin/bash
#Script to submit abaqus jobs via python script
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16g
#SBATCH --time=1:00:00
 

#below use Linux commands, which will run on compute node
cd ${SLURM_SUBMIT_DIR}
#load modules and export to paths so can call the TexGen functions
module load GCCcore/6.3.0
module load binutils/2.27-GCCcore-6.3.0
export PATH=/gpfs01/home/emxghs/bin:$PATH
export LD_LIBRARY_PATH=/gpfs01/home/emxghs/Python-2.7.16/Lib/site-packages/TexGen:$LD_LIBRARY_PATH

cd /gpfs01/home/emxghs/IAA3DWeaveProject
module load abaqus-uon/2018
#this should be complete
abq2018 cae noGUI=/gpfs01/home/emxghs/IAA3DWeaveProject/fitnessFun.py -- $1 $2 $3 $4 $5 ${6}
wait