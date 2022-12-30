#!/bin/bash

# create venv and install requirements into it
module load python/3.8.1
python3 -m venv ../venv
source ../venv/bin/activate

python -m pip install --upgrade pip
pip3 install -r ../requirements.txt

# kick of each thing we're testing in parallel
#sbatch sim_anneal.sh

# Tabu Search

#TABU_RDIR="output/tabu_search"
#TABU_DATE="$(date +%Y-%m-%d_%H-%M-%S)"
#export TABU_RUNDIR="$TABU_RDIR/$TABU_DATE"
#mkdir -p "$TABU_RUNDIR"/{img,json}

#sbatch tabu_search.sh

# Genetic Algorithm

#GENETIC_RDIR="output/genetic"
#GENETIC_DATE="$(date +%Y-%m-%d_%H-%M-%S)"
#export GENETIC_RUNDIR="$GENETIC_RDIR/$GENETIC_DATE"
#mkdir -p "$GENETIC_RUNDIR"/{img,json}
#
#bash genetic_launcher.sh

# Dispatching Rules
DISPATCH_RDIR="output/dispatching_rules"
DISPATCH_DATE="$(date +%Y-%m-%d_%H-%M-%S)"
export DISPATCH_RUNDIR="$DISPATCH_RDIR/$DISPATCH_DATE"
mkdir -p "$DISPATCH_RUNDIR"/{img,json,results}

bash dispatching_launcher.sh


# Constraint Programming (Google OR Tools)

#sbatch constraint.sh