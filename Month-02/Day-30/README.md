# 📅 Day 30 — Month 02: Model Context Protocol (MCP) Architecture

> Build a production Model Context Protocol (MCP) implementation adhering to JSON-RPC 2.0 specifications: MCP Server, MCP Client, Tools discovery and execution, Resource URI providers, and integration demos. Master Graph Shortest Path algorithms (LC 743 Dijkstra, LC 787 Bellman-Ford) in Java.

---

## 📁 Architecture Overview

```
Day-30/
├── mcp/
│   ├── server.py             # JSON-RPC 2.0 MCP Server
│   ├── client.py             # MCP Client interface
│   ├── tools.py              # Tool schema definitions & execution handlers
│   ├── resources.py          # URI-based context resource manager
│   └── schemas.py            # Protocol dataclass definitions
├── examples/
│   └── mcp_tool_demo.py      # End-to-end client/server test demo
├── DSA/
│   └── GraphShortestPath.java # LC 743 + LC 787 (Java)
├── Interview/
│   └── technical_questions.md # MCP architecture & Graph algorithms Q&A
├── Notes/
│   └── notes.md              # Protocol engineering deep-dive
└── README.md
```

---

## 🚀 Execution & Verification

### 1. Test MCP Client & Server Lifecycle (Python)
```bash
python Month-02/Day-30/examples/mcp_tool_demo.py
```

### 2. Compile & Run Java Graph Suite
```bash
cd Month-02/Day-30/DSA
javac GraphShortestPath.java && java DSA.GraphShortestPath
```
