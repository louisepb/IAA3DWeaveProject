#!/bin/bash
#SBATCH -p defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=10g
#SBATCH --time=168:00:00

 

module load matlab-uon/r2019b

 

cd $SLURM_SUBMIT_DIR

 

matlab -nodisplay -nosplash < start_optimisation.m




