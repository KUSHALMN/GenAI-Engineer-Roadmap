# Day 06 Notes: Stateful Agent Design

## 1. Core State Components
- `session_id`: Unique correlation ID across logs and subtasks.
- `status`: State machine enum enforcing valid transitions.
- `messages`: Conversation history and system prompts.
- `tool_cache`: Results of previously executed idempotent tools.
- `step_count`: Guard against runaway loops.
