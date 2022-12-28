#!/bin/bash
#SBATCH -a 1-1998
#SBATCH -o stdio/tabu_search-stdout-%A-%a.txt
#SBATCH -e stdio/tabu_search-stderr-%A-%a.txt
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=00:35:00
#SBATCH --partition=parallel
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=mcdermtimo@ecs.vuw.ac.nz

#VALUES=({0..2000})
#VALUES=({1998..3996})
ACCESS_KEY=${VALUES[$SLURM_ARRAY_TASK_ID]}

echo "++ Loading Python environment"
module load python/3.8.1
source ../venv/bin/activate

echo "++ Change directory"
cd ../src/Solvers/genetic || exit 1
echo "++ Starting program"
pwd
OUTPUT_DIR="../../../jobs/$GENETIC_RUNDIR" RUN_KEY="$ACCESS_KEY" python3 -u genetic_entry.py
# To get through all instances you have to manually batch the slurm ids, ie 1-1001, 1002-2002, 2003-3003, etc.
# Match the number of ids to the number of inputs in the file for that script