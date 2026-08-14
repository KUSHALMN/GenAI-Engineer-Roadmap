import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "rag_collection"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3
