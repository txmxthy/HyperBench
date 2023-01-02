#!/bin/bash
#SBATCH -a 1-1801
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

cd ../src/Solvers/simu || exit 1
OUTPUT_DIR="../../../jobs/output/sim_anneal" python3 simu_entry.py
