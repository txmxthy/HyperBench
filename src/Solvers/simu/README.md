# Job shop scheduling #
https://github.com/deeshumakholiya/PSSAI
- Run via terminal from the directory `jobshop_assignment` calling `python main.py`.
- Used Simulated Anneling as the alogorithm for this

### Adaptation for Paper
Local running: 
```commandline
SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/sim_anneal python3 simu_entry.py                 
```
* Timeout param is the number of seconds each dataset will run for.
* Total time for a single run is N Datasets * Timeout - we have 10 datasets. 


Multiply these by the number of full runs with a parameter setting we want to do.

Params: Temp, Cooldown
* 30 Seeds per hyper param setting. https://www.calculator.net/sample-size-calculator.html?type=1&cl=80&ci=5&pp=50&ps=&x=67&y=17
* 3 params for temp and 3 for cooldown with 30 seeds = 9 * 30 = 270 runs
* 270 * 10 datasets = 2700 runs
* Unwrapped dataset loop to allow them to run parallel and added to param file generator.

FINAL Time for alg = 2700 * timeout = 2700 * 60 = 162000 seconds = 45 hours worst case
Expected time for est 300 tasks concurrent = 162000 / 300 = 540 seconds = 9 minutes


Parameter settings:
* https://www.researchgate.net/publication/220743071_Simulated_annealing_its_parameter_settings_and_the_longest_common_subsequence_problem
  * In [14] the author suggests to use a high initial temperature and a cooldown factor between 0.8 and 0.99 for solving optimization problems in practice.  
  * 14] K. Weicker. Evolution¨are Algorithmen. Teubner Verlag, 2002.
