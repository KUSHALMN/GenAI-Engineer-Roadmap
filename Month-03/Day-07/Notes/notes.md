# 📅 Day 07 Notes — SSE Token Streaming & Kth Smallest in BST

## 🧠 What I Learned
1. **SSE Protocol Formatting:**
   - Headers: `Content-Type: text/event-stream`, `Cache-Control: no-cache`, `X-Accel-Buffering: no` (disables Nginx buffering).
   - Format: `data: <json>\n\n`.
   - Termination: Standard convention is `data: [DONE]\n\n`.
   - Keepalive: `: ping\n\n` comments prevent gateway timeouts (e.g. AWS ALB 60s idle timeout).
2. **Kth Smallest in BST:**
   - Inorder visits BST in sorted order.
   - Morris Traversal enables $\mathcal{O}(1)$ extra space traversal by creating temporary predecessor threads and dismantling them upon second visit.
