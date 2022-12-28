#!/bin/bash
#SBATCH -a 1-1001
#SBATCH -o stdio/sim_anneal-stdout-%A-%a.txt
#SBATCH -e stdio/sim_anneal-stderr-%A-%a.txt
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=00:35:00
#SBATCH --partition=parallel
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=mcdermtimo@ecs.vuw.ac.nz

module load python/3.8.1
source ../venv/bin/activate

cd ../src/Solvers/tabu || exit 1
OUTPUT_DIR="../../../jobs/output/tabu_search" python3 tabu_entry.py
# To get through all instances you have to manually batch the slurm ids, ie 1-1001, 1002-2002, 2003-3003, etc.
# Match the number of ids to the number of inputs in the file for that script