-- Select all users
SELECT * FROM users;

-- Select specific columns
SELECT name, email FROM users;

-- Filter with WHERE
SELECT * FROM users WHERE age > 25;

-- Order results
SELECT * FROM users ORDER BY age DESC;

-- Limit results
SELECT * FROM users LIMIT 2;

-- Search by name
SELECT * FROM users WHERE name LIKE 'A%';

-- Count users
SELECT COUNT(*) AS total_users FROM users;
