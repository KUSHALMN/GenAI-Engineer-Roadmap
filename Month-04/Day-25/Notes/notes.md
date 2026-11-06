# Day 25 Notes: Agent Sandboxing and Side-Effect Control

## 1. Sandbox Defenses
- Root directory jail (`os.path.abspath`).
- Journaling for atomic rollback.
- Simulation dry-run flags.
