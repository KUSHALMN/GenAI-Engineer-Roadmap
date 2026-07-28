# Day 6 Notes — GenAI Engineer Roadmap

## Topics Learned

### SQL Basics
- **DDL** — Data Definition Language: CREATE, DROP, ALTER
- **DML** — Data Manipulation Language: INSERT, UPDATE, DELETE
- **DQL** — Data Query Language: SELECT
- **Primary Key** — unique identifier for each row
- **SERIAL** — auto-incrementing integer in PostgreSQL
- **Constraints** — NOT NULL, UNIQUE, CHECK, DEFAULT

---

## SQL Practice

### CREATE TABLE
```sql
CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    age   INT CHECK (age >= 0)
);
```

### INSERT
```sql
INSERT INTO users (name, email, age) VALUES ('Kushal', 'k@example.com', 22);
```

### SELECT with filters
```sql
SELECT * FROM users WHERE age > 25 ORDER BY age DESC LIMIT 5;
```

### UPDATE
```sql
UPDATE users SET age = 23 WHERE id = 1;
```

### DELETE
```sql
DELETE FROM users WHERE id = 1;
```

---

## DSA (Java)

### Two Sum — LeetCode #1
- Approach: HashMap O(n)
- Store complement → index, check if current exists in map

### Contains Duplicate — LeetCode #217
- Approach: HashSet O(n)
- `set.add()` returns false if duplicate exists

### Intersection of Two Arrays — LeetCode #349
- Approach: HashSet O(n)
- Add nums1 to set, check nums2 against set

### Top K Frequent Elements — LeetCode #347
- Approach: HashMap + Min-Heap O(n log k)
- Count frequencies, use min-heap of size k

---

## AI Project — User Database (Python + PostgreSQL)

- Connected to PostgreSQL using `psycopg2`
- Full CRUD: create table, insert, read, update, delete
- Used `.env` for secure DB credentials
- `executemany()` for bulk inserts
- `ON CONFLICT DO NOTHING` to avoid duplicate email errors

---

## Key Takeaway
SQL is the language of data. Every AI application eventually needs a database — knowing SQL is non-negotiable for a GenAI engineer.
