![image](https://raw.githubusercontent.com/txmxthy/HyperBench/master/Hyperbench%20Logos/open-graph-logo.png)
# Welcome to HyperBench
- HyperBench is a framework for benchmarking and comparing solvers for the Job Shop Problem.
- It was specifically designed to allow for widespread parameter testing and comparison of traditional exact solvers against meta/hyper-herustics.

- The hyperbench framework includes automated grid job batching, time forecasting, some bundled solvers and examples for importing your own algorithm.
- Credit to the original authors for the implementation of their respective solvers or algorithms. I do not claim ownership of any external solvers or algorithms included. All rights are retained by their respective creators, and any use or distribution should acknowledge them accordingly.

- A simulation environment is also included which can be connected to the rendering mechanisms, or new algorithms can be built on the pre-existing environments.


# Dependencies

sudo apt-get install gifsicle on linux or https://eternallybored.org/misc/gifsicle/ on windows


# Running with SLURM.

To pull and run after cloning.
```commandline
git fetch && git reset --hard origin/master && bash batch.sh
```

To monitor slurm jobs
```commandline
squeue -u $USER -o "%.15i %.10P  %.16j %.7C %.7m %.12M %.12L %.10T %R"
```

To monitor slurm ids (Current Tasks)
```commandline
cat genetic-stderr-* | grep Slurm | grep -Eo '[0-9]{1,4}'
```
as above but sorted to get highest max
```commandline
cat genetic-stderr-* | grep Slurm | grep -Eo '[0-9]{1,4}' | sort -n | tail -n 1
```


# Local Running:

Tested and developed with Pycharm on debian/kali.

I suggest using an env file plugin to connect your IDE to the configuration file. During local running your computer will act as if it was a single node in the SLURM system, and the env file will provide the arguments which would typically come from the grid management script.

See: https://github.com/Ashald/EnvFile



## Simulated Annealing
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/<Path To>/HyperBench/jobs/output/sim_anneal RUN_KEY=1 python3 simu_entry.py    
```

## Tabu Search
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/<Path To>/HyperBench/jobs/output/tabu_search python3 tabu_entry.py    
```

## Genetic Algorithm
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/<Path To>/HyperBench/jobs/output/genetic python3 genetic_entry.py    
```

## Dispatching Rules
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/<Path To>/HyperBench/jobs/output/dispatching_rules python3 dispatching_rules_entry.py    
```

## Constraint 
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/<Path To>/HyperBench/jobs/output/constraint python3 constraint_entry.py    
```
# Parameter Selection
The default parameters have been selected from a range of literature. 
There is an accompanying report to this project which may be made public at some stage in the future. 

## Genetic Algorithm parameters
https://eprints.ncl.ac.uk/file_store/production/56840/02F80BF2-FA85-49F3-B5B4-3E63CB6A4412.pdf
https://www.researchgate.net/figure/Genetic-algorithm-parameters-and-their-values-types_tbl2_266204025

## Dispatching parameters
https://www.researchgate.net/publication/273266719_Comparison_of_dispatching_rules_in_job-shop_Schedulingproblem_Usingsimulation_A_case_study
