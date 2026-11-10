"""
Authentication Fundamentals: JWT Token Generation, Expiration,
HMAC-SHA256 Signing, Password Hashing, and Revocation Blocklist.
"""

from dataclasses import dataclass, field
import hashlib
import hmac
import json
import base64
import time
from typing import Dict, Optional, Set


@dataclass
class TokenPayload:
    sub: str
    tenant_id: str
    roles: list
    exp: float
    iat: float = field(default_factory=time.time)


class JWTAuthService:
    def __init__(self, secret_key: str, token_ttl_seconds: int = 3600):
        self.secret_key = secret_key.encode("utf-8")
        self.token_ttl = token_ttl_seconds
        self.revoked_tokens: Set[str] = set()

    def hash_password(self, password: str, salt: str = "secure_salt") -> str:
        return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

    def generate_token(self, user_id: str, tenant_id: str, roles: list) -> str:
        header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode("utf-8")).decode("utf-8").rstrip("=")
        now = time.time()
        payload_data = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "roles": roles,
            "iat": now,
            "exp": now + self.token_ttl
        }
        payload = base64.urlsafe_b64encode(json.dumps(payload_data).encode("utf-8")).decode("utf-8").rstrip("=")
        signature = hmac.new(self.secret_key, f"{header}.{payload}".encode("utf-8"), hashlib.sha256).hexdigest()
        return f"{header}.{payload}.{signature}"

    def verify_token(self, token: str) -> Optional[Dict]:
        if token in self.revoked_tokens:
            return None
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, payload, signature = parts
        expected_sig = hmac.new(self.secret_key, f"{header}.{payload}".encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None
        
        # Add padding back if necessary
        padded_payload = payload + "=" * ((4 - len(payload) % 4) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded_payload).decode("utf-8"))
        if time.time() > data.get("exp", 0):
            return None
        return data

    def revoke_token(self, token: str):
        self.revoked_tokens.add(token)


if __name__ == "__main__":
    auth = JWTAuthService(secret_key="production_super_secret_key", token_ttl_seconds=10)
    tok = auth.generate_token("user_101", "tenant_corp", ["admin", "developer"])
    claims = auth.verify_token(tok)
    assert claims is not None and claims["sub"] == "user_101"
    
    auth.revoke_token(tok)
    assert auth.verify_token(tok) is None
    print("=== Day 02: JWT Auth Service ===")
    print("Token verification & revocation blocklist passed.")
