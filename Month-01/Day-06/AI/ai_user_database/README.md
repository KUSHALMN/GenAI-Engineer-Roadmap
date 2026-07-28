# AI User Database

A Python + PostgreSQL CRUD app for managing users.

## Setup

```bash
pip install psycopg2-binary python-dotenv
```

Create `.env`:
```
DB_HOST=localhost
DB_NAME=genai_roadmap
DB_USER=postgres
DB_PASSWORD=your_password
```

## Run in Order

```bash
python create_table.py   # Create users table
python insert_user.py    # Insert sample users
python get_users.py      # View all users
python update_user.py    # Update a user
python delete_user.py    # Delete a user
```
