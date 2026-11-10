# 📝 Notes — Day 09: Docker Hardening & Concurrency

## 1. Container Security Checklist
- Run as non-root user (`USER appuser`).
- Never run Docker daemon with `--privileged`.
- Mount root filesystem as read-only (`--read-only`) with writable `/tmp` tmpfs.
- Scan images using Trivy or Grype in CI pipelines before registry push.
