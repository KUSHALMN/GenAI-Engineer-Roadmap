import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

while True:
    questions = input("Ask me anything: ")
    if questions.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": questions}
        ]
    )

    print("AI:", response.choices[0].message.content)
