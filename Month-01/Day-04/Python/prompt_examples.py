from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 1. Zero-shot prompting
print("=== Zero-Shot ===")
print(ask("Translate 'Hello, how are you?' to French."))

# 2. Few-shot prompting
print("\n=== Few-Shot ===")
few_shot_prompt = """
Classify the sentiment as Positive, Negative, or Neutral.

Text: "I love this product!" → Positive
Text: "This is terrible." → Negative
Text: "It works fine." → Neutral
Text: "Absolutely amazing experience!" →
""".strip()
print(ask(few_shot_prompt))

# 3. Chain-of-thought prompting
print("\n=== Chain-of-Thought ===")
cot_prompt = "If a train travels 60 km/h for 2.5 hours, how far does it go? Think step by step."
print(ask(cot_prompt))

# 4. System role prompting
print("\n=== System Role ===")
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a Python expert who explains concepts simply."},
        {"role": "user", "content": "What is a decorator in Python?"}
    ]
)
print(response.choices[0].message.content)
