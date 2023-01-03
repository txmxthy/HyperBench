#!/bin/bash
#SBATCH --job-name=CONSTRAINT_JSS
#SBATCH -a 1-12
#SBATCH -o stdio/constraint-stdout-%A-%a.txt
#SBATCH -e stdio/constraint-stderr-%A-%a.txt
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=2G
#SBATCH --time=00:35:00
#SBATCH --partition=parallel
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=mcdermtimo@ecs.vuw.ac.nz

ACCESS_KEY=$SLURM_ARRAY_TASK_ID

# Log to STDERR
echo "++ Running Slurm ID: $SLURM_ARRAY_TASK_ID" >&2
echo "Key: $ACCESS_KEY" >&2
# Dump Values array


module load python/3.8.1
source ../venv/bin/activate
cd ../src/Solvers/constraint || exit 1

RELATIVE="../../../jobs/$CONSTRAINT_RUNDIR"
echo "++ Relative path: $RELATIVE" >&2

OUTPUT_DIR=$RELATIVE RUN_KEY="$ACCESS_KEY" python3 -u constraint_entry.py
# To get through all instances you have to manually batch the slurm ids, ie 1-1001, 1002-2002, 2003-3003, etc.
# Match the number of ids to the number of inputs in the file for that script
