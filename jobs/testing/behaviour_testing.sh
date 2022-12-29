#!/bin/bash

PARAMS="../src/Solvers/genetic/genetic_inputs.txt"
PARAM_COUNT=67501
MAX_BATCH_SIZE=1998
BATCH_COUNT=$((PARAM_COUNT / MAX_BATCH_SIZE))
REMAINING=$((PARAM_COUNT % MAX_BATCH_SIZE))

echo "++BATCH_COUNT" "$BATCH_COUNT"

# Loop to check if there are any remaining parameters to run
while [ "$REMAINING" -gt 0 ]; do
    # If there are remaining parameters, add a batch and subtract the max batch size from the remaining
    echo "++ REMAINING: $REMAINING"

    BATCH_COUNT=$((BATCH_COUNT + 1))
    REMAINING=$((REMAINING - MAX_BATCH_SIZE))
done

echo "++BATCH_COUNT" "$BATCH_COUNT"

run_batch() {
  local start="$1"
  local end="$2"
  local slurm="$3"
  local batch="$4"

  echo "$start..$end: $slurm | $batch"
}

# Batch_count -1 for 0 indexing
LIMIT=$((BATCH_COUNT - 1))

for i in $(seq 14 $LIMIT); do
  START=$(($i * $MAX_BATCH_SIZE))
  END=$(($START + $MAX_BATCH_SIZE))

  if [ "$END" -gt "$PARAM_COUNT" ]; then
    END="$PARAM_COUNT"
    # Change the slurm array to only run the remaining parameters
    # Subtract remaining from max batch size (Remaining will be negative)
    MAX_BATCH_SIZE=$(($MAX_BATCH_SIZE + $REMAINING))
  fi

  run_batch $START $END $MAX_BATCH_SIZE $i
done

# run_batch $END $((END + REMAINING))

