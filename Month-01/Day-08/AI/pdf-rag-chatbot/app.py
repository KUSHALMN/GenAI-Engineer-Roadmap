import os
from groq import Groq
from dotenv import load_dotenv
from pdf_loader import load_pdf
from chunking import chunk_by_words
from vector_store import add_chunks, search

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant. Answer questions using only the provided context.
If the answer is not in the context, say 'I don't know'."""

def load_and_index(pdf_path: str):
    print(f"📄 Loading: {pdf_path}")
    text = load_pdf(pdf_path)
    chunks = chunk_by_words(text, chunk_size=200, overlap=30)
    add_chunks(chunks)

def ask(question: str) -> str:
    context_chunks = search(question, n_results=3)
    context = "\n\n".join(context_chunks)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    pdf_path = "sample.pdf"
    if not os.path.exists(pdf_path):
        print("⚠️  Place a sample.pdf in this directory to test.")
    else:
        load_and_index(pdf_path)
        print("\n🤖 PDF RAG Chatbot — type 'exit' to quit\n")
        while True:
            question = input("You: ")
            if question.lower() == "exit":
                break
            print(f"Bot: {ask(question)}\n")
