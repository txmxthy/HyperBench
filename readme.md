# JSS Comparison Project

# Grid running

To pull and run after cloning.
```commandline
git fetch && git reset --hard origin/master && bash batch.sh
```

to monitor slurm jobs
```commandline



# Local Running:


## Simulated Annealing
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/sim_anneal python3 simu_entry.py    
```

## Tabu Search
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/tabu_search python3 tabu_entry.py    
```

## Genetic Algorithm
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/genetic python3 genetic_entry.py    
```