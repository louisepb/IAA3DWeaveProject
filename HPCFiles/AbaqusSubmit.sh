#!/bin/bash
#SBATCH --chdir="/gpfs01/home/emxghs/AbaqusRunParallel"
#SBATCH -p defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=44g
#SBATCH --time=4:00:00

module load intel/compiler/2017
first="$1"
echo "The first argument :  $first"

/software/abaqus/abaqus.sh -cores 8 -machines 1 -machmem 44gb -time 4:00:00 -ver 2021 -partition defq -file $1 -arguments user=MPC.for