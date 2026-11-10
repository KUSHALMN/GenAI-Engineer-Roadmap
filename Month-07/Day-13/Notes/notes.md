# 📝 Notes — Day 13: CI Pipelines & Runtime Reflection

## 1. Production CI Pipeline Topology
1. **Fast Fail (1-2m):** Flake8, Ruff, MyPy, Prettier.
2. **Deterministic Tests (3-5m):** PyTest unit tests with mocked LLM APIs.
3. **Container Build & Scan (5m):** Docker build + Trivy vulnerability scanning.
4. **Model Eval Suite (10m):** Parallel evaluation against golden Q&A dataset.
