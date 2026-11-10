# 📝 Notes — Day 25: Production RAG Deployment & Defensive Coding

## 1. Kubernetes Container Lifecycle
- Define `initialDelaySeconds` and `failureThreshold` on startup probes to prevent premature pod restarts during model weight initialization.
