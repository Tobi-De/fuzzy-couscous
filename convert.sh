#!/bin/bash

for file in docs/guides/*; do
    if [ -f "$file" ]; then
        new_file=$(echo "$file" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
        mv "$file" "$new_file"
    fi
done
