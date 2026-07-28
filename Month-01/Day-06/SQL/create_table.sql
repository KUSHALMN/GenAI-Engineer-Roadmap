-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id        SERIAL PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    email     VARCHAR(150) UNIQUE NOT NULL,
    age       INT CHECK (age >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
