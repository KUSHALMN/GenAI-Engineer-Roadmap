# Day 34 Notes — Month 02, Day 02
## Topic: Docker + JWT Auth + Climbing Stairs DP

---

## AI: Docker + JWT Authentication

### JWT Flow
```
POST /auth/token  →  verify password  →  create JWT  →  return token
GET  /protected   →  extract Bearer   →  decode JWT  →  return data
```

### JWT Security Checklist
- [ ] SECRET_KEY in env var, never hardcoded
- [ ] Short expiry (15-30 min) + refresh tokens
- [ ] Explicit algorithm in decode: `algorithms=["HS256"]`
- [ ] Blocklist on logout via Redis jti
- [ ] No sensitive data in payload

### Docker Layer Caching Order
```dockerfile
FROM python:3.11-slim        # base layer
COPY requirements.txt .      # deps layer (cached)
RUN pip install ...          # install layer (cached)
COPY src/ .                  # code layer (invalidates on change)
CMD [...]
```

### Key Commands
```bash
docker build -t genai-api .
docker run -p 8000:8000 -e SECRET_KEY=mysecret genai-api
docker-compose up --build
pytest tests/test_auth.py -v
```

---

## DSA: Climbing Stairs (LC 70) — DP

### Recurrence
```
dp[i] = dp[i-1] + dp[i-2]   (Fibonacci)
```

### Complexity
- Time: O(n) | Space: O(1) after optimization

### Pattern Family
- Fibonacci DP → Decode Ways → Min Cost Climbing Stairs → Tribonacci
