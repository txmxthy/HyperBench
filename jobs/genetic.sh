#!/bin/bash
#SBATCH --job-name=GA_JSS
#SBATCH -a 1-20
#SBATCH -o stdio/genetic-stdout-%A-%a.txt
#SBATCH -e stdio/genetic-stderr-%A-%a.txt
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=00:35:00
#SBATCH --partition=parallel
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=mcdermtimo@ecs.vuw.ac.nz


#VALUES=({0..2000})

# Replace the above with a loop to generate between passed in environment variables

VALUES=()
for i in $(seq $START $END); do
    VALUES+=("$i")
done

num_elements=${#VALUES[@]}
sorted_values=($(printf "%s\n" "${VALUES[@]}" | sort -n))
lowest=${sorted_values[0]}
highest=${sorted_values[-1]}
printf "Verified: %s, %s-%s\n" "$num_elements" "$lowest" "$highest"


ACCESS_KEY=${VALUES[$SLURM_ARRAY_TASK_ID]}
module load python/3.8.1
source ../venv/bin/activate
cd ../src/Solvers/genetic || exit 1
OUTPUT_DIR="../../../jobs/$GENETIC_RUNDIR" RUN_KEY="$ACCESS_KEY" python3 -u genetic_entry.py
# To get through all instances you have to manually batch the slurm ids, ie 1-1001, 1002-2002, 2003-3003, etc.
# Match the number of ids to the number of inputs in the file for that script