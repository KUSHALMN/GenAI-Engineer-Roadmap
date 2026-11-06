# Day 02 Notes: Reliable Tool Dispatcher

## 1. Dispatcher Pattern Responsibilities
A robust tool dispatcher acts as the middleware between LLM outputs and backend services:
- **Registration & Schema Generation:** Maintains active registry of available functions.
- **Argument Parsing & Coercion:** Casts incoming stringified types (e.g., `"10"` -> `10`) when permitted.
- **Normalized Contract Output:** Always produces uniform JSON payloads containing `success`, `data`, and `error`.
- **Fault Tolerance:** Prevents user input errors or external API 500s from terminating the agent loop.
