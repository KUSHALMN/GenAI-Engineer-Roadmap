import os
from rag_pipeline import ingest, query
from config import PDF_PATH

if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        print("⚠️  Place a sample.pdf in this directory to test.")
    else:
        ingest(PDF_PATH)
        print("\n🤖 PDF RAG Chatbot — type 'exit' to quit\n")
        while True:
            question = input("You: ")
            if question.lower() == "exit":
                break
            print(f"Bot: {query(question)}\n")
