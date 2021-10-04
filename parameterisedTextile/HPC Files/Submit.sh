#!/bin/bash
#Script to submit abaqus jobs via python script
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=6
#SBATCH --mem=32g
#SBATCH --time=6:00:00
 

#below use Linux commands, which will run on compute node
cd ${SLURM_SUBMIT_DIR}

module load abaqus-uon/2018

/software/abaqus/abaqus.sh -cores 6 -machines 1 -machmem 32gb -time 6:00:00 -partition defq  -jobname weave1 -file $1.inp


wait

