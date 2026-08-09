# Month 1 - Day 12

## Topics Learned
- JWT Authentication with FastAPI
- Linked List DSA patterns (Reverse, Middle)
- Modular Auth API architecture

## DSA (Java)
- Reverse Linked List — LeetCode #206
- Middle of Linked List — LeetCode #876

## AI Project
- AI Auth API (FastAPI + JWT)
  - `config.py` — environment and settings management
  - `models.py` — database models
  - `database.py` — database connection setup
  - `auth.py` — JWT authentication logic
  - `routes.py` — API routes for auth endpoints
  - `app.py` — FastAPI app entry point

## Interview Prep
- technical_questions.md — JWT auth, Linked List DSA
- coding_questions.md — Java & Python problems

## What I Learned
Built a production-ready JWT auth API with FastAPI. Linked List problems reinforced pointer manipulation — reverse in-place and find middle using slow/fast pointers.

---

## Folder Structure

```
Day-12/
├── AI/
│   └── ai-auth-api/
│       ├── app.py
│       ├── auth.py
│       ├── config.py
│       ├── database.py
│       ├── models.py
│       ├── routes.py
│       ├── requirements.txt
│       └── README.md
├── DSA/
│   ├── reverse_linked_list.java
│   └── middle_of_linked_list.java
├── Interview/
│   ├── technical_questions.md
│   └── coding_questions.md
├── Notes/
│   └── notes.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/reverse_linked_list.java && java -cp DSA reverse_linked_list
javac DSA/middle_of_linked_list.java && java -cp DSA middle_of_linked_list
```

**AI Auth API:**
```bash
cd AI/ai-auth-api
pip install -r requirements.txt
# Add .env with SECRET_KEY and DATABASE_URL
python app.py
```
