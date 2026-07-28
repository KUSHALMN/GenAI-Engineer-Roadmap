import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "genai_roadmap"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

users = [
    ("Kushal", "kushal@example.com", 22),
    ("Alice", "alice@example.com", 25),
    ("Bob", "bob@example.com", 30),
]

cur.executemany(
    "INSERT INTO users (name, email, age) VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING",
    users
)

conn.commit()
print(f"✅ Inserted {cur.rowcount} users.")
cur.close()
conn.close()
