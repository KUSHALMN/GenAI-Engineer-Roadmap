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

# Get all users
cur.execute("SELECT id, name, email, age FROM users ORDER BY id")
users = cur.fetchall()

print("All Users:")
print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Age'}")
print("-" * 55)
for user in users:
    print(f"{user[0]:<5} {user[1]:<15} {user[2]:<25} {user[3]}")

cur.close()
conn.close()
