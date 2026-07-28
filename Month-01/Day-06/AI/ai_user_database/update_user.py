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
new_age = 23
new_name = "Kushal MN"

cur.execute(
    "UPDATE users SET name = %s, age = %s WHERE id = %s",
    (new_name, new_age, user_id)
)

conn.commit()
print(f"✅ Updated user id={user_id} → name='{new_name}', age={new_age}")
cur.close()
conn.close()
