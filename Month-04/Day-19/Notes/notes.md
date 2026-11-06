# Day 19 Notes: Connect LLM Tool Selection to MCP

## 1. Pipeline
1. Query MCP `tools/list`.
2. Convert to target provider schema.
3. Pass tools into LLM completion call.
4. Model emits function call.
5. Bridge invokes MCP `tools/call`.
6. Return formatted result message.
