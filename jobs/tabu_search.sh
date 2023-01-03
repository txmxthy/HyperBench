#!/bin/bash
#SBATCH --job-name=Tabu_Search
#SBATCH -a 1-1998
#SBATCH -o stdio/tabu_search-stdout-%A-%a.txt
#SBATCH -e stdio/tabu_search-stderr-%A-%a.txt
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=00:35:00
#SBATCH --partition=parallel
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=mcdermtimo@ecs.vuw.ac.nz

# First value of array is skipped
VALUES=({1..1998})
ACCESS_KEY=${VALUES[$SLURM_ARRAY_TASK_ID]}


echo "++ Loading Python environment"
module load python/3.8.1
source ../venv/bin/activate

echo "++ Change directory"
cd ../src/Solvers/tabu || exit 1
echo "++ Starting program"
pwd
OUTPUT_DIR="../../../jobs/$TABU_RUNDIR" RUN_KEY="$ACCESS_KEY" python3 -u tabu_entry.py
