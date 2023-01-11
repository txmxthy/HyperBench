#!/bin/bash

# create venv and install requirements into it
module load python/3.8.1
python3 -m venv ../venv
source ../venv/bin/activate

python -m pip install --upgrade pip
pip3 install -r ../requirements.txt

STAMP="$(date +%Y-%m-%d_%H-%M-%S)"

# kick of each thing we're testing in parallel
#SIM_RDIR="output/sim_anneal"
#export SIM_RUNDIR="$SIM_RDIR/$STAMP"
#mkdir -p "$SIM_RUNDIR"/{img,json,csv}
#sbatch sim_anneal.sh

# Tabu Search

#TABU_RDIR="output/tabu_search"
#export TABU_RUNDIR="$TABU_RDIR/$STAMP"
#mkdir -p "$TABU_RUNDIR"/{img,json,results}

#sbatch tabu_search.sh
#
# Genetic Algorithm
#
#GENETIC_RDIR="output/genetic"
#export GENETIC_RUNDIR="$GENETIC_RDIR/$STAMP"
#mkdir -p "$GENETIC_RUNDIR"/{img,json}
#
#bash genetic_launcher.sh

# Dispatching Rules
#DISPATCH_RDIR="output/dispatching_rules"
#export DISPATCH_RUNDIR="$DISPATCH_RDIR/$STAMP"
#mkdir -p "$DISPATCH_RUNDIR"/{img,json,results}
#
#bash dispatching_launcher.sh


# Constraint Programming (Google OR Tools)
#CONSTRAINT_RDIR="output/constraint"
#export CONSTRAINT_RUNDIR="$CONSTRAINT_RDIR/$STAMP"
#mkdir -p "$CONSTRAINT_RUNDIR"/{img,json,results}
#sbatch constraint.sh


#
# Genetic Programming
#
#GP_RDIR="output/gp"
#export GP_RUNDIR="GP_RDIR/$STAMP"
#mkdir -p "GP_RUNDIR"/{img,json}
#
#bash gp_launcher.sh