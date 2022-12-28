#!/bin/bash
# Utility script to batch up genetic runs with large paramter inputs

# Divide the parameter file line count by the max batch size to get the number of batches
# Param file = /home/kali/PycharmProjects/Capstone/src/Solvers/genetic/genetic_inputs.txt

PARAMS="../src/Solvers/genetic/genetic_inputs.txt"
PARAM_COUNT=$(wc -l < "$PARAMS")

# scontrol show config | grep -i array | grep -Eo '[0-9]{1,4}'
#MAX_BATCH_SIZE=$(scontrol show config | grep -i array | grep -Eo '[0-9]{1,4}')
MAX_BATCH_SIZE=2000
# Subtract 1 from the max batch size to account for the first line being skipped
MAX_BATCH_SIZE=$((MAX_BATCH_SIZE - 2))
# Get the number of batches required to run all the parameters (without any remainder)
BATCH_COUNT=$((PARAM_COUNT / MAX_BATCH_SIZE))

# Echo
echo "++ Parameter file: $PARAMS"
echo "++ Parameter count: $PARAM_COUNT"
echo "++ Max batch size: $MAX_BATCH_SIZE"
echo "++ Batch count: $BATCH_COUNT"

# Loop through the batches
for i in $(seq 0 $BATCH_COUNT); do
    # Calculate the start and end of the batch
    START=$((i * MAX_BATCH_SIZE + 1))
    END=$((START + MAX_BATCH_SIZE - 1))
    # If the end is greater than the parameter count, set it to the parameter count
    if [ "$END" -gt "$PARAM_COUNT" ]; then
        END="$PARAM_COUNT"
    fi
    # Echo
    echo "++ Batch $i: $START - $END"
    # Submit the batch
    START="$START" END="$END" bash genetic.sh
done



