#!/bin/bash
#SBATCH -p defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem=12g
#SBATCH --time=168:00:00





#below use Linux commands, which will run on compute node
cd ${SLURM_SUBMIT_DIR}

#load modules and export to paths so can call the TexGen functions
module load GCCcore/6.3.0
module load binutils/2.27-GCCcore-6.3.0
export PATH=/gpfs01/home/emxghs/bin:$PATH
export LD_LIBRARY_PATH=/gpfs01/home/emxghs/Python-2.7.16/Lib/site-packages/TexGen:$LD_LIBRARY_PATH

cd /gpfs01/home/emxghs/AbaqusRunParallel
module load abaqus-uon/2018
abaqus cae noGUI=fitnessFun.py -- 3 4 1 1 4 2
