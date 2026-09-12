# 📅 Day 34 — Month 02, Day 02: Docker + JWT Auth + Climbing Stairs DP

> Build a production-ready FastAPI app with JWT authentication, containerized with Docker. Master Climbing Stairs (LC 70) Fibonacci DP in Java.

---

## 📁 Structure

```
Day-02/
├── src/
│   └── main.py             # FastAPI app with JWT login, /me, /protected endpoints
├── tests/
│   └── test_auth.py        # 8 unit tests for auth endpoints
├── DSA/
│   └── ClimbingStairs.java # LC 70 + k-step variant — O(1) space DP (Java)
├── Interview/
│   ├── technical_questions.md  # JWT security, Docker layers, CMD vs ENTRYPOINT
│   └── coding_questions.md     # Climbing Stairs recurrence, k-steps, related problems
├── Notes/
│   └── notes.md
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🧠 AI: JWT Auth API

### Run Locally
```bash
cd Month-02/Day-02
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Run with Docker
```bash
docker build -t genai-auth-api .
docker run -p 8000:8000 -e SECRET_KEY=mysecret genai-auth-api
# or
docker-compose up --build
```

### Run Tests
```bash
pytest tests/test_auth.py -v
```

### API Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | No | Health check |
| POST | `/auth/token` | No | Login → JWT token |
| GET | `/me` | Bearer | Current user info |
| GET | `/protected` | Bearer | Protected resource |

---

## ☕ DSA: Climbing Stairs — LC 70 (Java)

**Pattern**: Fibonacci DP — O(n) time, O(1) space

```
dp[i] = dp[i-1] + dp[i-2]
```

### Run
```bash
cd Month-02/Day-02/DSA
javac ClimbingStairs.java
java ClimbingStairs
```

**Expected output:**
```
1
2
3
8
89
4
13
```

---

## 🎯 Key Takeaways

1. **JWT** is stateless but needs Redis blocklist for proper logout/revocation.
2. **Docker layer order** matters — put deps before source code for cache efficiency.
3. **Climbing Stairs = Fibonacci** — recognizing this pattern unlocks Decode Ways, Min Cost Stairs, Tribonacci.
4. **`alg: none` attack** — always explicitly pass `algorithms=["HS256"]` to `jwt.decode()`.

---

## ✅ Status: Done
