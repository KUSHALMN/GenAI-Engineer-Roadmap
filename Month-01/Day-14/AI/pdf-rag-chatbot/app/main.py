import os
from app.rag_pipeline import ingest, query

DOCS_DIR = "sample_documents"

for filename in os.listdir(DOCS_DIR):
    if filename.endswith(".pdf"):
        ingest(os.path.join(DOCS_DIR, filename))

while True:
    q = input("\nAsk: ").strip()
    if q.lower() == "exit":
        break
    print("Answer:", query(q))
