# JSS Comparison Project


# Deps

sudo apt-get install gifsicle on linux or https://eternallybored.org/misc/gifsicle/ on windows


# Grid running

To pull and run after cloning.
```commandline
git fetch && git reset --hard origin/master && bash batch.sh
```

to monitor slurm jobs
```commandline
squeue -u $USER -o "%.15i %.10P  %.16j %.7C %.7m %.12M %.12L %.10T %R"
```

to monitor slurm ids
```commandline
cat genetic-stderr-* | grep Slurm | grep -Eo '[0-9]{1,4}'
```
as above but sorted to get highest max
```commandline
cat genetic-stderr-* | grep Slurm | grep -Eo '[0-9]{1,4}' | sort -n | tail -n 1
```


# Local Running:

Tested and developed with pycharm on debian.
To run via pycharm seamlessly you can use the env file plugin and edit the run configuration to specify the variables as per the env file/commands below.
See: https://github.com/Ashald/EnvFile

## Simulated Annealing
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/sim_anneal RUN_KEY=1 python3 simu_entry.py    
```

## Tabu Search
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/tabu_search python3 tabu_entry.py    
```

## Genetic Algorithm
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/genetic python3 genetic_entry.py    
```

## Dispatching Rules
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/dispatching_rules python3 dispatching_rules_entry.py    
```

## Constraint 
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/constraint python3 constraint_entry.py    
```

# Ga parameters
https://eprints.ncl.ac.uk/file_store/production/56840/02F80BF2-FA85-49F3-B5B4-3E63CB6A4412.pdf
https://www.researchgate.net/figure/Genetic-algorithm-parameters-and-their-values-types_tbl2_266204025

# Dispatching Params
https://www.researchgate.net/publication/273266719_Comparison_of_dispatching_rules_in_job-shop_Schedulingproblem_Usingsimulation_A_case_study