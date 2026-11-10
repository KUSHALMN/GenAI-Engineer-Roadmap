"""
Docker Production Practices: Multi-stage Dockerfile parser,
non-root user verification, minimal base image audit, and healthcheck linter.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class DockerAuditReport:
    is_multi_stage: bool
    runs_as_non_root: bool
    has_healthcheck: bool
    uses_pinned_versions: bool
    security_score: int
    recommendations: List[str]


class DockerHardenerLinter:
    def audit_dockerfile(self, dockerfile_content: str) -> DockerAuditReport:
        lines = dockerfile_content.splitlines()
        from_stages = [l for l in lines if l.strip().upper().startswith("FROM")]
        is_multi_stage = len(from_stages) > 1

        runs_as_non_root = any("USER " in l.upper() and "ROOT" not in l.upper() for l in lines)
        has_healthcheck = any(l.strip().upper().startswith("HEALTHCHECK") for l in lines)
        uses_pinned_versions = all(":" in l and ":latest" not in l for l in from_stages)

        recommendations = []
        score = 100
        if not is_multi_stage:
            score -= 25
            recommendations.append("Adopt multi-stage builds to exclude compiler toolchains from production image.")
        if not runs_as_non_root:
            score -= 30
            recommendations.append("Add 'USER appuser' to prevent container breakout privilege escalation.")
        if not has_healthcheck:
            score -= 20
            recommendations.append("Define HEALTHCHECK instruction for container orchestrator liveness probes.")
        if not uses_pinned_versions:
            score -= 25
            recommendations.append("Pin base image tags with explicit SHA-256 digests instead of ':latest'.")

        return DockerAuditReport(
            is_multi_stage=is_multi_stage,
            runs_as_non_root=runs_as_non_root,
            has_healthcheck=has_healthcheck,
            uses_pinned_versions=uses_pinned_versions,
            security_score=max(0, score),
            recommendations=recommendations
        )


if __name__ == "__main__":
    hardened_dockerfile = """
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -u 1001 appuser
USER appuser
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY app ./app
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app"]
    """
    linter = DockerHardenerLinter()
    report = linter.audit_dockerfile(hardened_dockerfile)
    assert report.security_score == 100
    assert report.runs_as_non_root is True
    print("=== Day 09: Docker Production Hardener ===")
    print("Dockerfile linter passed with 100/100 security rating.")
