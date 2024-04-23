import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_URL")
DEBUG_APP = True
MODEL_NAME = "llama3"
CHROMA_PATH = "chroma"
DATA_PATH = "data"
USE_OPENAI_EMBEDDING = False
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")