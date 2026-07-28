# Month 1 - Day 6

## Topics Learned
- SQL Basics (DDL, DML, DQL)
- PostgreSQL — CREATE, INSERT, SELECT, UPDATE, DELETE
- Python + PostgreSQL with psycopg2
- DSA — HashMap & HashSet patterns

## SQL
- create_database.sql
- create_table.sql
- insert.sql
- select.sql
- update.sql
- delete.sql

## DSA (Java)
- Two Sum — LeetCode #1
- Contains Duplicate — LeetCode #217
- Intersection of Two Arrays — LeetCode #349
- Top K Frequent Elements — LeetCode #347

## AI Project
- Full CRUD User Database with Python + PostgreSQL

## What I Learned
Today I learned SQL from scratch and connected Python to PostgreSQL using psycopg2. Built a full CRUD user management system. On the DSA side, practiced HashMap and HashSet patterns which are the foundation of many array problems.

---

## Folder Structure

```
Day-06/
├── SQL/
│   ├── create_database.sql
│   ├── create_table.sql
│   ├── insert.sql
│   ├── select.sql
│   ├── update.sql
│   └── delete.sql
├── DSA/
│   ├── two_sum.java
│   ├── contains_duplicate.java
│   ├── intersection_arrays.java
│   └── top_k_frequent.java
├── AI/
│   └── ai_user_database/
│       ├── create_table.py
│       ├── insert_user.py
│       ├── get_users.py
│       ├── update_user.py
│       ├── delete_user.py
│       └── README.md
├── Notes/
│   └── day6_notes.md
├── Resources.md
└── README.md
```

## How to Run

**SQL (PostgreSQL):**
```bash
psql -U postgres -f SQL/create_database.sql
psql -U postgres -d genai_roadmap -f SQL/create_table.sql
psql -U postgres -d genai_roadmap -f SQL/insert.sql
psql -U postgres -d genai_roadmap -f SQL/select.sql
```

**DSA (Java):**
```bash
javac DSA/two_sum.java && java -cp DSA two_sum
javac DSA/contains_duplicate.java && java -cp DSA contains_duplicate
javac DSA/intersection_arrays.java && java -cp DSA intersection_arrays
javac DSA/top_k_frequent.java && java -cp DSA top_k_frequent
```

**AI User Database:**
```bash
cd AI/ai_user_database
pip install psycopg2-binary python-dotenv
# Create .env with DB credentials
python create_table.py
python insert_user.py
python get_users.py
python update_user.py
python delete_user.py
```
