# 📅 Day 42 — Month 02, Day 12: MCP (Model Context Protocol)

> Build a minimal MCP-style tool server exposing system telemetry and calculator tools over JSON-RPC 2.0, a client that dynamically discovers and invokes them, tool argument validation, and security guidelines. Implement Heap and Priority Queue patterns in Python and Java.

---

## 📁 Structure

```
Day-12/
├── mcp_server.py           # JSON-RPC 2.0 MCP server with tools/list and tools/call
├── mcp_client.py           # MCP client for tool discovery and safe execution
├── tools/
│   ├── system_metrics.py   # Safe read-only host telemetry tool
│   └── calculator.py       # Arithmetic calculation tool
├── mcp_security_notes.md   # Threat modeling, sandboxing, and permission boundaries for MCP
├── heap_patterns.py        # Top K (LC 347), Kth Largest (LC 215), Merge K Lists (LC 23)
├── README.md
└── DSA/
    └── HeapPatterns.java   # Heap patterns in Java (LC 215, LC 347, LC 23)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python mcp_server.py
python mcp_client.py
python heap_patterns.py
```

### Java Tests
```bash
cd DSA
javac HeapPatterns.java
java HeapPatterns
```

---

## ✅ Status: Completed
