from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat(user_message, history=[]):
    history.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history
    )
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply, history

history = []
print("Groq Chat — type 'exit' to quit\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    reply, history = chat(user_input, history)
    print(f"AI: {reply}\n")
