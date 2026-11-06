# Day 01 Notes: Agent Architecture and Tool Contract Design

## 1. The Autonomy Spectrum
| Pattern | Adaptability | Determinism | Latency/Cost | Best Use Case |
|---|---|---|---|---|
| Router | Low | Very High | Lowest | Direct intent categorization |
| State Machine | Medium | High | Predictable | Form-filling, multi-step workflows |
| ReAct | Very High | Low | Variable/High | Open-ended search, debugging |
| Plan & Solve | High | Medium | Moderate | Complex multi-stage research |

## 2. Tool Contract Architecture
A production tool contract requires:
1. **Name & Docstring:** High semantic clarity so the LLM correctly associates user intent with the tool.
2. **Typed Parameter Specification:** Standard JSON schema properties with data types and enum constraints.
3. **Semantic Tags:**
   - `idempotent`: True if calling multiple times with same arguments yields identical side effects.
   - `has_side_effects`: True if external state (files, DB, external APIs) is modified.
   - `rate_limit_per_minute`: Prevents agent runaway loops from overloading downstream APIs.
