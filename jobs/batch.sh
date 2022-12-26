#!/bin/bash

# create venv and install requirements into it
module load python/3.8.1
python3 -m venv ../venv
source ../venv/bin/activate

python -m pip upgrade pip
pip3 install -r ../requirements.txt

# kick of each thing we're testing in parallel
#sbatch constraint.sh
#sbatch genetic.sh
sbatch sim_anneal.sh
#sbatch tabu_search.sh

