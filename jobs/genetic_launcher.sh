#!/bin/bash
# Utility script to batch up genetic runs with large paramter inputs

# Divide the parameter file line count by the max batch size to get the number of batches
# Param file = /home/kali/PycharmProjects/Capstone/src/Solvers/genetic/genetic_inputs.txt

PARAMS="../src/Solvers/genetic/genetic_inputs.txt"
#PARAM_COUNT=$(wc -l < "$PARAMS")
PARAM_COUNT=20


# Get start time
START_TIME=$(date +%s)


#MAX_BATCH_SIZE=$(scontrol show config | grep -i array | grep -Eo '[0-9]{1,4}')
# Subtract 2 from the max batch size to account for the first line being skipped and slurm being dumb
MAX_BATCH_SIZE=7 #@TODO This isnt working and associated numbers are off too!
# Get the number of batches required to run all the parameters as a float and round up
BATCH_COUNT=$((PARAM_COUNT / MAX_BATCH_SIZE))
REMAINING=$((PARAM_COUNT % MAX_BATCH_SIZE))

# Loop to check if there are any remaining parameters to run
while [ "$REMAINING" -gt 0 ]; do
    # If there are remaining parameters, add a batch and subtract the max batch size from the remaining
    BATCH_COUNT=$((BATCH_COUNT + 1))
    REMAINING=$((REMAINING - MAX_BATCH_SIZE))
done

# Echo
echo "++ Parameter file: $PARAMS"
echo "++ Parameter count: $PARAM_COUNT"
echo "++ Max batch size: $MAX_BATCH_SIZE"
echo "++ Batch count: $BATCH_COUNT"


# Loop through the batches
LIMIT=$((BATCH_COUNT - 1))
for i in $(seq 0 $LIMIT); do
    # Calculate the start and end of the batch
    START=$((i * MAX_BATCH_SIZE))
    END=$((START + MAX_BATCH_SIZE))
    # If the end is greater than the parameter count, set it to the parameter count
    if [ "$END" -gt "$PARAM_COUNT" ]; then
        END="$PARAM_COUNT"
        # Change the slurm array to only run the remaining parameters
        # Subtract remaining from max batch size (Remaining will be negative)
        MAX_BATCH_SIZE=$((MAX_BATCH_SIZE + REMAINING))
    fi
    # Echo
    echo "++ Batch $i: $START - $END"
    # Submit the batch
    START="$START" END="$END" BATCH=$i sbatch -a 1-$MAX_BATCH_SIZE genetic.sh

    # Wait for the batch to finish

    # Count the number of jobs in the queue with the job name
    NUM_JOBS=1
    # While there are still jobs in the queue with the job name
    while [ "$NUM_JOBS" -gt 0 ]; do
        NUM_JOBS=$(squeue -u $USER -o "%.15i %.10P  %.16j %.7C %.7m %.12M %.12L %.10T %R" | grep "JSS" -c)
        echo "++ Waiting for batch $i to finish. $NUM_JOBS jobs in queue."
        sleep 30
        NUM_JOBS=$(squeue -u $USER -o "%.15i %.10P  %.16j %.7C %.7m %.12M %.12L %.10T %R" | grep "JSS" -c)
    done
    echo "++ Batch $i finished."
done
# Get end time
END_TIME=$(date +%s)
# Calculate the time taken
TIME_TAKEN=$((END_TIME - START_TIME))
# Echo
echo "++ All batches finished in $TIME_TAKEN seconds."



