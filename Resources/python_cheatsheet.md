# Python Cheatsheet — Month 01

## OOP

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
```

## File I/O

```python
# Read file
with open("file.txt", "r") as f:
    content = f.read()

# Write file
with open("file.txt", "w") as f:
    f.write("Hello")
```

## List Comprehensions

```python
squares = [x**2 for x in range(10)]
evens   = [x for x in range(10) if x % 2 == 0]
```

## Collections

```python
from collections import Counter, defaultdict

# Count frequency
freq = Counter(["a", "b", "a", "c", "a"])  # Counter({'a': 3, ...})

# Default dict
d = defaultdict(int)
d["key"] += 1
```

## Regular Expressions

```python
import re
tokens = re.findall(r'\b[a-z]+\b', text.lower())
```

## FastAPI Pattern

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

## psycopg2 Pattern

```python
import psycopg2

conn = psycopg2.connect(host="localhost", database="db", user="postgres", password="pass")
cur = conn.cursor()
cur.execute("SELECT * FROM users WHERE id = %s", (1,))
rows = cur.fetchall()
conn.commit()
cur.close()
conn.close()
```

## Environment Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
```
