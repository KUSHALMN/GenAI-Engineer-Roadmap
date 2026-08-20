# Tool-Calling AI Assistant (Day 19)

A modular, production-grade Tool-Calling / Function-Calling Assistant built with Python and compatible with OpenAI and Groq function-calling APIs.

---

## 🌟 Overview

Large Language Models (LLMs) cannot natively perform precise arithmetic, access up-to-date databases, or interact with external systems. **Tool Calling** (Function Calling) allows an LLM to recognize when an external tool is required, output structured JSON specifying the tool name and arguments, and incorporate the tool's execution result back into its response generation loop.

```
┌──────────┐     User Query      ┌───────────┐
│   User   │ ──────────────────> │    LLM    │
└──────────┘                     └─────┬─────┘
                                       │ Tool Call (JSON: calculate("sqrt(144) + 10"))
                                       ▼
┌──────────────┐   Result: "22"   ┌────────────────┐
│ LLM Response │ <─────────────── │ Tool Execution │
└──────────────┘                  └────────────────┘
```

---

## 🏗️ Architecture & Modules

| File | Purpose |
| :--- | :--- |
| `schemas.py` | Pydantic data models for OpenAI-compatible tools, function calls, and chat message structures. |
| `tool_registry.py` | Automatic reflection-based JSON schema generator from Python type hints and safe dispatcher. |
| `tools/calculator.py` | AST-based mathematical expression evaluator without insecure `eval()`. |
| `tools/chat_history.py` | Conversation memory lookup, keyword search, and episodic summary storage. |
| `llm.py` | Agent orchestration loop handling iterative tool calling, error handling, and API integration. |
| `app.py` | Interactive CLI interface supporting automated demo mode and manual dialogue. |

---

## 🚀 Getting Started

### 1. Installation

```bash
cd Month-01/Day-19/AI/tool-calling-assistant
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional)

Create a `.env` file or export your API key:
```bash
# For Groq (Fast LLaMA 3.3 70B inference)
GROQ_API_KEY=gsk_your_groq_api_key_here

# OR for OpenAI
OPENAI_API_KEY=sk-your_openai_api_key_here
```
> **Note**: If no API key is provided, the assistant automatically switches to a built-in mock simulation mode so you can test and inspect the tool-calling flow without credentials.

### 3. Run the Assistant

**Run the Automated Demo:**
```bash
python app.py --demo
```

**Run Interactive Chat:**
```bash
python app.py
```

---

## 🛠️ How Tool Calling Works Step-by-Step

1. **Registration & Schema Derivation**:
   Python functions are registered with `@registry.register`. The system inspects parameter names, types, and docstrings to build a standard JSON Schema.
2. **First LLM Call**:
   The prompt and tools array are sent to the model with `tool_choice="auto"`.
3. **Tool Call Detection**:
   If the LLM emits `tool_calls`, the agent pauses text generation, parses the arguments, and executes the target function via `ToolRegistry.execute()`.
4. **Tool Message Append**:
   The tool output is appended to the message list with `role="tool"` and matching `tool_call_id`.
5. **Second LLM Call**:
   The complete message chain is resent to the model so it can synthesize the final response incorporating the external tool result.
