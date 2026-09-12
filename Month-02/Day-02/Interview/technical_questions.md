# Day 34 (Month 02 - Day 02): Technical Interview Questions
## Focus: Docker, JWT Authentication, Production API Security

---

### Q1: How does JWT authentication work and what are its security risks?

**Answer:**
- **Flow**: User logs in → server creates JWT (header.payload.signature) signed with `SECRET_KEY` → client stores token → sends in `Authorization: Bearer <token>` header → server verifies signature and expiry.
- **Structure**:
  - `header`: algorithm + token type (base64)
  - `payload`: claims — `sub`, `exp`, `role` (base64, NOT encrypted)
  - `signature`: `HMAC_SHA256(header + payload, SECRET_KEY)`
- **Risks**:
  1. **Secret key exposure**: If `SECRET_KEY` leaks, attacker can forge any token. Store in env vars, never hardcode.
  2. **No revocation**: JWTs are stateless — a stolen token is valid until expiry. Mitigate with short TTL (15-30 min) + refresh tokens in Redis.
  3. **Algorithm confusion**: Always explicitly set `algorithms=["HS256"]` in `jwt.decode()` — prevents `alg: none` attack.
  4. **Payload exposure**: Never store sensitive data in JWT payload — it's base64, not encrypted.

---

### Q2: What is the difference between a Docker image and container, and how does layer caching work?

**Answer:**
- **Image**: Read-only blueprint — a stack of filesystem layers built from `Dockerfile` instructions.
- **Container**: A running instance of an image with a writable layer on top.
- **Layer caching**:
  - Each `RUN`, `COPY`, `ADD` creates a new cached layer.
  - **Best practice**: Copy `requirements.txt` before source code:
    ```dockerfile
    COPY requirements.txt .
    RUN pip install -r requirements.txt   # cached unless deps change
    COPY src/ .                           # only invalidates from here
    ```
  - Code changes don't trigger a full `pip install` rebuild.

---

### Q3: How do you handle token refresh and logout in a stateless JWT system?

**Answer:**
- **Refresh tokens**: Issue short-lived access token (15 min) + long-lived refresh token (7 days) stored in Redis.
- **Logout / revocation**: Add token `jti` (JWT ID) to a Redis blocklist on logout. Check blocklist on every request. TTL = remaining token lifetime.
- **Why not sessions?**: JWTs are stateless and horizontally scalable — no shared session store needed across API instances.

---

### Q4: What is the difference between `CMD` and `ENTRYPOINT` in a Dockerfile?

**Answer:**
- **`CMD`**: Default command — can be overridden at `docker run` time. Used for default arguments.
- **`ENTRYPOINT`**: Fixed executable — always runs. `CMD` becomes default args to `ENTRYPOINT`.
- **Best practice for APIs**:
  ```dockerfile
  ENTRYPOINT ["uvicorn"]
  CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
  Override port at runtime: `docker run api uvicorn main:app --port 9000`
