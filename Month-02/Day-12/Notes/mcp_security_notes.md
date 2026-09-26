# 🔒 Model Context Protocol (MCP) Security Notes

## 1. Threat Landscape of MCP Architecture
The Model Context Protocol connects LLM clients (such as Claude Desktop or IDEs) to local or remote tool servers over standard transports (stdio or HTTP with SSE).

### Key Vulnerabilities:
1. **Remote Code Execution (RCE)**: Tools that accept arbitrary shell or SQL strings can execute destructive actions if manipulated by prompt injection.
2. **Local File System Traversal**: Tools reading or writing files without strict directory chroot confinement can expose `/etc/shadow`, `.ssh/id_rsa`, or environment keys.
3. **Cross-Boundary Exfiltration**: A malicious prompt injection inside a tool result can trick the LLM into invoking a secondary tool that transmits data over network egress.

---

## 2. Security Best Practices

### A. Granular Tool Permissions
- Require explicit authorization tokens or user confirmations for high-risk capabilities (write operations, terminal commands, network fetches).
- Implement read-only role scopes by default.

### B. Input Validation Against JSON Schema
- Do not trust LLM argument payloads. Validate every argument against the tool's published JSON Schema prior to calling the underlying Python function.

### C. Sandboxing & Process Confinement
- Run untrusted tool servers in isolated Docker containers with no root privileges, read-only root filesystems, and bounded CPU/memory limits.
- Confine file operations to an explicit whitelisted working directory.

### D. Audit Logging & Structured Telemetry
- Log all JSON-RPC requests, including caller identity, timestamp, tool name, serialized arguments, execution latency, and return status codes.
