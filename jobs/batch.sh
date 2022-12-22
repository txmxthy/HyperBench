#!/bin/bash
#SBATCH -a 1-30 
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=00:10:00
#SBATCH --partition=parallel
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=mcdermtimo@ecs.vuw.ac.nz

bash constraint.sh
bash genetic.sh
bash sim_anneal.sh
bash tabu_search.sh

