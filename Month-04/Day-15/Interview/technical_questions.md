# Day 15: Technical Interview Preparation — MCP Protocol Fundamentals & Edit Distance

### Q1: What is the Model Context Protocol (MCP) and what problem does it solve?
**Answer:**
MCP is an open standard created to replace fragmented, proprietary tool-integration protocols. Instead of rewriting custom connectors for every model provider (OpenAI functions, Anthropic tool use, Gemini tools), developers write an MCP Server once. Any MCP Client / Host (IDE, agent, platform) can discover tools, read resources, and execute functions over standard JSON-RPC 2.0 transports (stdio or HTTP/SSE).

### Q2: What are the three core primitives exposed by an MCP Server?
**Answer:**
1. **Tools:** Executable functions with side effects or compute (e.g., `execute_sql()`).
2. **Resources:** Read-only data sources accessed via URI schemas (e.g., `file:///var/logs/system.log`).
3. **Prompts:** Parameterized system prompt templates for guiding model behaviors.
