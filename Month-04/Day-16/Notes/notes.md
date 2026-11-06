# Day 16 Notes: Build a Basic MCP Server

## 1. Handshake Flow
1. Client sends `initialize` request.
2. Server responds with protocol version and capabilities.
3. Client sends `notifications/initialized`.
4. Client queries `tools/list` and begins `tools/call` executions.
