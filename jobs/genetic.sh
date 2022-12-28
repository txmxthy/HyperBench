#!/bin/bash
#SBATCH --job-name=GA_JSS
#SBATCH -a 1-9
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
echo "" >&2
echo "=== Batch $BATCH ===" >&2
echo "inputs: $START - $END" >&2
VALUES=()
for i in $(seq $START $END); do
    VALUES+=("$i")
done


lowest=${VALUES[0]}
highest=${VALUES[-1]}
# Highest - lowest
num_elements=$((highest - lowest))
>&2 printf "Verified: %s, %s-%s\n" "$num_elements" "$lowest" "$highest"

# Check if the SLURM_ARRAY_TASK_ID is within the range of the values
if [ "$SLURM_ARRAY_TASK_ID" -gt "$num_elements" ]; then
    >&2 printf "ERROR: SLURM_ARRAY_TASK_ID %s is greater than the number of elements %s\n" "$SLURM_ARRAY_TASK_ID" "$num_elements"
    exit 1
fi

ACCESS_KEY=${VALUES[$SLURM_ARRAY_TASK_ID]}

# Log to STDERR
echo "++ Running Slurm ID: $SLURM_ARRAY_TASK_ID" >&2
echo "Key: $ACCESS_KEY" >&2
# Dump Values array
echo "Values: ${VALUES[0]} ... ${VALUES[-1]}" >&2


module load python/3.8.1
source ../venv/bin/activate
cd ../src/Solvers/genetic || exit 1
OUTPUT_DIR="../../../jobs/$GENETIC_RUNDIR" RUN_KEY="$ACCESS_KEY" python3 -u genetic_entry.py
# To get through all instances you have to manually batch the slurm ids, ie 1-1001, 1002-2002, 2003-3003, etc.
# Match the number of ids to the number of inputs in the file for that script