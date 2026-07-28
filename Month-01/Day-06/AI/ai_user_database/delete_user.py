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

user_id = 1
cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

conn.commit()
print(f"✅ Deleted user id={user_id}")
cur.close()
conn.close()
