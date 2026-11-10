"""
API Rate Limiting & Quotas: Token Bucket Algorithm, Per-Tenant Token Allowances,
Concurrency Throttling, and 429 Retry-After Envelopes.
"""

from dataclasses import dataclass
import time
from typing import Dict, Tuple


@dataclass
class TenantQuota:
    tokens_per_second: float
    max_burst_capacity: float
    current_tokens: float
    last_updated: float


class TenantQuotaLimiter:
    def __init__(self):
        self.quotas: Dict[str, TenantQuota] = {}

    def register_tenant(self, tenant_id: str, tps: float, burst: float):
        self.quotas[tenant_id] = TenantQuota(tps, burst, burst, time.time())

    def consume(self, tenant_id: str, tokens_requested: int = 1) -> Tuple[bool, float]:
        quota = self.quotas.get(tenant_id)
        if not quota:
            return False, 0.0

        now = time.time()
        elapsed = now - quota.last_updated
        quota.current_tokens = min(quota.max_burst_capacity, quota.current_tokens + elapsed * quota.tokens_per_second)
        quota.last_updated = now

        if quota.current_tokens >= tokens_requested:
            quota.current_tokens -= tokens_requested
            return True, 0.0

        retry_after = (tokens_requested - quota.current_tokens) / quota.tokens_per_second
        return False, round(retry_after, 2)


if __name__ == "__main__":
    limiter = TenantQuotaLimiter()
    limiter.register_tenant("tenant_pro", tps=10.0, burst=10.0)

    # Consume available burst
    allowed, retry = limiter.consume("tenant_pro", tokens_requested=10)
    assert allowed is True

    # Immediate next request throttled
    blocked, retry_after = limiter.consume("tenant_pro", tokens_requested=5)
    assert blocked is False
    assert retry_after > 0.0

    print("=== Day 16: Tenant Quota Limiter ===")
    print(f"Throttled request, Retry-After: {retry_after}s")
