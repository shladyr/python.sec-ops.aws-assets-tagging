#!/bin/bash

# Loop to create 100 files
for i in {1..100}; do
  # Create a file with the name pattern "number.aws.soc2.prompt"
  touch "$i.aws.soc2.prompt"
done

echo "100 files created with the pattern 'number.aws.soc2.prompt'"
