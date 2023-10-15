#!/bin/bash

# Output file
AUTHORS_FILE="AUTHORS"

# Ensure the AUTHORS file is empty or doesn't exist
> "$AUTHORS_FILE"

# Use Git log to extract contributor names and emails
git log --format='%aN <%aE>' | sort -u >> "$AUTHORS_FILE"

echo "AUTHORS file generated."
