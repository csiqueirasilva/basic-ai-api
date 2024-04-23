#!/bin/bash
set -e

# Start the Ollama service in the background
/bin/ollama serve &

# Function to check if the Ollama service is ready
ollama_service_is_ready() {
  for i in {1..10}; do
    # Using curl to send a GET request to the Ollama service
    response=$(curl -s http://localhost:11434)

    # Check if the response contains "Ollama is running"
    if [[ "$response" == *"Ollama is running"* ]]; then
      return 0
    else
      sleep 1
    fi
  done

  echo "Ollama service failed to start after 10 tries."
  return 1
}

# Wait for Ollama service to be ready
if ! ollama_service_is_ready; then
  echo "Ollama service is not ready, exiting..."
  exit 1
fi

# Pull the required Ollama model
ollama pull llama3
ollama pull nomic-embed-text

# Directory containing your model files
MODEL_FILES_DIR="./modelfiles"

# Loop through each file in the directory
for file in "$MODEL_FILES_DIR"/*; do
  if [[ -f "$file" ]]; then
    # Extract the base name of the file for use as the model name
    model_name=$(basename "$file")

    # Create and run the model with ollama using the model_name
    ollama create "$model_name" -f "$file"
    ollama run "$model_name"
  fi
done

echo "Startup finished"

# Now, wait Ollama to finish
wait $!