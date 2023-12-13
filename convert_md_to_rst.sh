#!/bin/bash

# Specify the folder containing the markdown files
folder="docs/guides"

# Loop through all the markdown files in the folder
for file in "$folder"/*.md; do
    # Get the filename without the extension
    filename=$(basename "$file" .md)
    
    # Convert the markdown file to rst using pandoc
    pandoc --wrap=preserve "$file" -f markdown -t rst -o "$folder/$filename".rst
done
