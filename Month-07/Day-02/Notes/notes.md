# 📝 Notes — Day 02: Authentication Fundamentals & Creational Patterns

## 1. Token Mechanics
- **Header:** Base64URL encoded JSON containing algorithm (`alg`) and token type (`typ`).
- **Payload:** Claims such as `sub` (subject), `tenant_id`, `roles`, `iat` (issued-at), `exp` (expiration).
- **Signature:** Cryptographic signature calculated using `HMAC-SHA256(secret, header.payload)`.
- **Revocation Strategies:** Short-lived access tokens (15m) + Redis blocklist for revoked refresh tokens.

## 2. Creational Patterns Trade-offs
- **Singleton:** Eliminates redundant connection overhead, but can make unit tests interdependent if state is mutable.
- **Builder:** Ideal for objects with 4+ optional parameters, guaranteeing immutability.
