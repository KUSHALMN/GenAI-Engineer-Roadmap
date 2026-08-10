from rag_pipeline import ingest, query

PDF_PATH = "sample.pdf"

ingest(PDF_PATH)

while True:
    q = input("\nAsk: ").strip()
    if q.lower() == "exit":
        break
    print("Answer:", query(q))
