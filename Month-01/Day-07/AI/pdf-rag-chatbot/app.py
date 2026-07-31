import os
from groq import Groq
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from pdf_loader import load_pdf
from chunking import chunk_by_words

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("pdf_rag")

def load_and_index(pdf_path: str):
    print(f"Loading PDF: {pdf_path}")
    text = load_pdf(pdf_path)
    chunks = chunk_by_words(text, chunk_size=200, overlap=30)
    embeddings = model.encode(chunks).tolist()
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    print(f"Indexed {len(chunks)} chunks.")

def retrieve(query: str, n_results: int = 3) -> list[str]:
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results["documents"][0]

def ask(question: str) -> str:
    context_chunks = retrieve(question)
    context = "\n\n".join(context_chunks)

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer questions using only the provided context. If the answer is not in the context, say 'I don't know'."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    pdf_path = "sample.pdf"
    if not os.path.exists(pdf_path):
        print("Place a sample.pdf in this directory to test.")
    else:
        load_and_index(pdf_path)
        print("\nPDF RAG Chatbot — type 'exit' to quit\n")
        while True:
            question = input("You: ")
            if question.lower() == "exit":
                break
            answer = ask(question)
            print(f"Bot: {answer}\n")
