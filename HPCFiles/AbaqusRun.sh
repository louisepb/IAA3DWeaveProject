#!/bin/bash
#SBATCH --chdir="/gpfs01/home/emxghs/AbaqusRunParallel"
#SBATCH -p defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=12g
#SBATCH --time=168:00:00





#below use Linux commands, which will run on compute node
cd ${SLURM_SUBMIT_DIR}
module load matlab-uon/r2019b


#load modules and export to paths so can call the TexGen functions
module load GCCcore/6.3.0
module load binutils/2.27-GCCcore-6.3.0
export PATH=/gpfs01/home/emxghs/Python-3.9.9/bin:$PATH
export LD_LIBRARY_PATH=/gpfs01/home/emxghs/Python-3.9.9/lib/python3.9/site-packages/TexGen:$LD_LIBRARY_PATH

cd /gpfs01/home/emxghs/AbaqusRunParallel
module load abaqus-uon/2018

matlab -nodisplay -nosplash < start_optimisation.m