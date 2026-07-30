# SQL Cheatsheet — Month 01

## DDL — Data Definition Language

```sql
-- Create table
CREATE TABLE users (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) UNIQUE NOT NULL,
    age        INT CHECK (age >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Drop table
DROP TABLE users;

-- Add column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
```

## DML — Data Manipulation Language

```sql
-- Insert single
INSERT INTO users (name, email, age) VALUES ('Kushal', 'k@example.com', 22);

-- Insert multiple
INSERT INTO users (name, email, age) VALUES
    ('Alice', 'alice@example.com', 25),
    ('Bob',   'bob@example.com',   30);

-- Update
UPDATE users SET age = 23 WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
```

## DQL — Data Query Language

```sql
-- Select all
SELECT * FROM users;

-- Select columns
SELECT name, email FROM users;

-- Filter
SELECT * FROM users WHERE age > 25;

-- Order
SELECT * FROM users ORDER BY age DESC;

-- Limit
SELECT * FROM users LIMIT 5;

-- Count
SELECT COUNT(*) FROM users;

-- Like (pattern match)
SELECT * FROM users WHERE name LIKE 'A%';

-- Between
SELECT * FROM users WHERE age BETWEEN 20 AND 30;
```

## Constraints

| Constraint | Description |
|------------|-------------|
| PRIMARY KEY | Unique + Not Null identifier |
| UNIQUE | No duplicate values |
| NOT NULL | Value required |
| CHECK | Custom condition |
| DEFAULT | Fallback value |
| FOREIGN KEY | Reference another table |

## PostgreSQL CLI

```bash
psql -U postgres                    # connect
\c dbname                           # switch database
\dt                                 # list tables
\d tablename                        # describe table
\q                                  # quit
```
