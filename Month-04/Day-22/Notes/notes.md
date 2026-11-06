# Day 22 Notes: MCP Long-Running Tasks and Notifications

## 1. Asynchronous Lifecycle
- `tools/call` -> emits `task_id`
- Server streams `notifications/progress`
- Client emits `tasks/cancel` if timeout threshold breached.
