import psycopg2
from config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id         SERIAL PRIMARY KEY,
            username   VARCHAR(50) UNIQUE NOT NULL,
            email      VARCHAR(150) UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tables created.")

def get_user_by_username(username: str) -> dict | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, hashed_password FROM users WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "email": row[2], "hashed_password": row[3]}
    return None

def create_user(username: str, email: str, hashed_password: str) -> dict:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s) RETURNING id",
        (username, email, hashed_password)
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": user_id, "username": username, "email": email}
