import time
from typing import Dict, Tuple

class TokenBucketRateLimiter:
    def __init__(self, rpm_limit: int = 60, tpm_limit: int = 50000):
        self.rpm_limit = rpm_limit
        self.tpm_limit = tpm_limit
        self._tenants: Dict[str, Dict] = {}

    def _get_tenant_state(self, tenant_id: str) -> Dict:
        now = time.time()
        if tenant_id not in self._tenants:
            self._tenants[tenant_id] = {
                "request_tokens": float(self.rpm_limit),
                "token_budget": float(self.tpm_limit),
                "last_refill": now
            }
        state = self._tenants[tenant_id]
        elapsed = now - state["last_refill"]
        rpm_refill = (self.rpm_limit / 60.0) * elapsed
        tpm_refill = (self.tpm_limit / 60.0) * elapsed
        state["request_tokens"] = min(float(self.rpm_limit), state["request_tokens"] + rpm_refill)
        state["token_budget"] = min(float(self.tpm_limit), state["token_budget"] + tpm_refill)
        state["last_refill"] = now
        return state

    def consume(self, tenant_id: str, estimated_tokens: int = 100) -> Tuple[bool, str]:
        state = self._get_tenant_state(tenant_id)
        if state["request_tokens"] < 1.0:
            return False, f"RPM limit exceeded for tenant '{tenant_id}'"
        if state["token_budget"] < float(estimated_tokens):
            return False, f"TPM quota exceeded for tenant '{tenant_id}'"
        state["request_tokens"] -= 1.0
        state["token_budget"] -= float(estimated_tokens)
        return True, "Allowed"
