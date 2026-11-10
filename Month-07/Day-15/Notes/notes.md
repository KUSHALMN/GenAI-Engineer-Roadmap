# 📝 Notes — Day 15: Secrets Management & Low-Level Design

## 1. Secrets Management Rules
- Never commit `.env` or plaintext tokens to Git repositories.
- Use pre-commit hooks (`git-secrets` or `gitleaks`) to block API key commits.
- Configure log sanitization middleware to scrub keys matching standard token patterns.
