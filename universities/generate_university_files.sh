#!/bin/bash

# Ensure a filename argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 filename.txt"
    exit 1
fi

while IFS= read -r university
do
    python3 create_md.py "$university"
done < "$1"

