import os
from dotenv import load_dotenv

load_dotenv()

# LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

# Embedding
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Vector Store
COLLECTION_NAME = "pdf_rag"
N_RESULTS = 3

# Chunking
CHUNK_SIZE = 200
OVERLAP = 30

# PDF
PDF_PATH = "sample.pdf"
