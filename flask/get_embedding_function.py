from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings
from constants import OLLAMA_BASE_URL, OPENAI_API_KEY, USE_OPENAI_EMBEDDING

def get_embedding_function():

    # another way to use remote embeddings from original code
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )

    # local embeddings
    embeddings = None

    if USE_OPENAI_EMBEDDING and OPENAI_API_KEY:
        # another way to calculate remote embeddings
        embeddings = OpenAIEmbeddings(api_key = OPENAI_API_KEY, model = "text-embedding-3-small")
    else:
        embeddings = OllamaEmbeddings(model="nomic-embed-text",base_url=OLLAMA_BASE_URL)

    return embeddings