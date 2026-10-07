# 📅 Day 27 Study Notes: Guardrails Architecture & Advanced Tree Traversals

## 🧠 Core Engineering Principles

### 1. Guardrail Execution Lifecycle
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant InGuard as Input Guardrail
    participant Model as LLM Engine
    participant OutGuard as Output Guardrail
    participant HITL as Tool HITL Gate

    User->>InGuard: Prompt (Text)
    InGuard->>InGuard: PII Scan, Injection, Topic Rules
    alt Violation Detected
        InGuard-->>User: 400 Policy Exception
    else Input Clean
        InGuard->>Model: Verified Prompt
        Model->>OutGuard: Raw Output / Tool Calls
        OutGuard->>OutGuard: Schema Validation & Leak Check
        opt Tool Execution
            OutGuard->>HITL: High-Risk Permission Check
            HITL-->>OutGuard: Approved by Admin
        end
        OutGuard-->>User: Validated Response
    end
```

### 2. Schema Validation Strategies
1. **Syntactic Validation**: Verifying that the LLM payload is well-formed JSON string.
2. **Structural Validation**: Ensuring all required schema keys are present.
3. **Semantic / Type Validation**: Checking that fields conform to integer, float, string, or boolean constraints without hallucinated extra keys.

### 3. Tree Recursion Invariants (Java)
- Diameter & Path Sum problems require tracking two quantities simultaneously:
  1. The global maximum answer discovered so far that spans *through* the current node as an inverted "V".
  2. The single linear branch sum returned up to the parent caller ($val + \max(left, right)$).
