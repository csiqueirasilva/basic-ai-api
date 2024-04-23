#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

cd /app  # Ensure the script is running in the /app directory.

# Note: Generating the database when starting the container can be costly with APIs like OpenAPI. 
# Be cautious to not overwrite previously generated databases unless intended.

# Directory containing model directories
MODEL_DIRS_DIR="./data"

# Loop through each entry in the directory
for entry in "$MODEL_DIRS_DIR"/*; do
  if [[ -d "$entry" ]]; then
    model_name=$(basename "$entry")
    echo "Generating embeddings for $model_name"
    python populate_database.py --dir "$model_name" --reset
  else
    echo "$entry is not a directory"
  fi
done

# Execute the main application
python app.py