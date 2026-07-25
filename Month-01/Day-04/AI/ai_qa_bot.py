from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions clearly and concisely.
If you don't know the answer, say 'I don't know' instead of making something up."""

def ask(question, history=[]):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    answer = response.choices[0].message.content
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    return answer, history

print("AI Q&A Bot — type 'exit' to quit\n")
history = []
while True:
    question = input("Question: ")
    if question.lower() == "exit":
        break
    answer, history = ask(question, history)
    print(f"Answer: {answer}\n")
