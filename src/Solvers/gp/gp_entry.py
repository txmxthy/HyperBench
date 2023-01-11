import os

from parameters.configure_params import configure_gp

with open("gp_inputs.csv", "r") as f:
    lines = f.readlines()

task_id = int(os.environ["RUN_KEY"])
print(f"Hello! This is GP with Coevolution - Task {task_id}")

# seed,eval.num-elites,generations,pop.subpops,select.tournament.size,filepath

seed, evalnelites, generations, selecttournamentsize, filepath = lines[task_id].split(',')

dictcfg = {
    "seed": seed,
    "eval.num-elites": evalnelites,
    "generations": generations,
    "select.tournament.size": selecttournamentsize,
    "filePath": filepath
}

timeout = 60 * 5
config_path = configure_gp(dictcfg, task_id)

# Run the GP
print(f"Running with 'java -jar GeneticProgramming.jar -file {config_path}")
os.system(f"java -jar GeneticProgramming.jar -file {config_path}")
# os.system(f"java -jar GeneticProgramming.jar -file {config_path}")

# @TODO: Rendering Schedules
# @TODO Env var for output dir
# @TODO: Edit JAVA to name schedule with env var for slurm
# @TODO: EDIT Java to output aveGenRulesize and Job.0.time with slurm, same as out.stat
# @TODO: Run on grid
