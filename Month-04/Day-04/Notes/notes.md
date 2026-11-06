# Day 04 Notes: ReAct Agent Loop Mechanics

## 1. Anatomy of a ReAct Loop
1. **User Goal:** Initial context supplied in system prompt.
2. **Scratchpad:** Accumulation of previous `Thought`, `Action`, and `Observation` triples.
3. **Model Generation:** Emits either next action or final conclusion.
4. **Tool Execution:** Dispatcher executes tool and formats observation.
5. **Observation Feedback:** Append observation to prompt context for next turn.

## 2. Guardrails
- Always set a hard ceiling `max_steps` to avoid unbounded cloud provider API bills.
