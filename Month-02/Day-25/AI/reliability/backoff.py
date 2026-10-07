"""Backoff calculation strategies with jitter to prevent thundering herd."""
import random
from typing import Optional


class ExponentialBackoff:
    """Calculates backoff delays with exponential growth and randomized full/equal jitter."""

    def __init__(
        self,
        base_delay: float = 0.5,
        max_delay: float = 8.0,
        factor: float = 2.0,
        jitter: bool = True
    ):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.factor = factor
        self.jitter = jitter

    def compute_delay(self, attempt: int) -> float:
        """Compute delay in seconds for the given zero-indexed attempt number."""
        calculated = min(self.max_delay, self.base_delay * (self.factor ** attempt))
        if self.jitter:
            # Full jitter: random uniform between 0 and calculated delay
            return round(random.uniform(0.1, calculated), 3)
        return round(calculated, 3)
