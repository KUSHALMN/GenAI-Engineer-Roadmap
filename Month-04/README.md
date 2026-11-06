# 📅 Month 04 — Agents, MCP & Tool-Use Engineering

> Topics: ReAct Loops, Planner-Executor Architectures, Tool Contracts & JSON Schemas, Dynamic Tool Dispatching, Stateful Workflow Graphs, Checkpointing & Recovery, Human-in-the-Loop Approval Gates, Concurrency & Parallel Execution, Multi-Tier Memory, Budget & Stopping Policies, Trajectory Evaluation, Model Context Protocol (MCP) JSON-RPC 2.0 Specifications, Stdio & SSE MCP Servers, MCP Resources & Prompts, MCP Client Integration, LLM Tool Bridges, Role-Based Access Control (RBAC), Security Threat Modeling & Injection Sanitization, Long-Running Asynchronous Tasks, Multi-Agent Topologies (Orchestrator-Worker, Peer-to-Peer), Delegation Contracts, Process Sandboxing, Distributed Observability & OpenTelemetry Tracing, Regression Suites, Enterprise Platform Architecture, and Capstone Benchmarking.

---

## 🎯 Day-by-Day Implementation Plan (Day 01 – Day 31)

| Day | GenAI / Agent & MCP Topic | Key Deliverables (Python in `AI/`) | DSA (Java in `DSA/`) | Status |
|:---:|:--------------------------|:-----------------------------------|:---------------------|:------:|
| [Day 01](Day-01/) | Agent Architecture & Tool Contracts | `tool_contract_validator.py` (JSON Schema, side-effects, idempotency) | Recursion Templates & Subsets (`SubsetsRecursion.java`) | ✅ Done |
| [Day 02](Day-02/) | Reliable Tool Dispatcher | `tool_dispatcher.py` (Registration, type casting, error normalization) | Backtracking — Subsets II Duplicates (`SubsetsWithDuplicates.java`) | ✅ Done |
| [Day 03](Day-03/) | Tool Selection & Intent Routing | `tool_router.py` (Semantic routing, ambiguity resolution, fallbacks) | Backtracking — Permutations (`Permutations.java`) | ✅ Done |
| [Day 04](Day-04/) | ReAct Agent Loop Mechanics | `react_loop.py` (Observe-Think-Act, scratchpad, max steps) | Backtracking — Combination Sum (`CombinationSum.java`) | ✅ Done |
| [Day 05](Day-05/) | Planner-Executor Pattern | `planner_executor.py` (Plan decomposition, status lifecycle, replan) | Grid Backtracking — Word Search (`WordSearch.java`) | ✅ Done |
| [Day 06](Day-06/) | Stateful Agent Design | `stateful_agent.py` (Immutable state, state-machine transitions) | Constraint Backtracking — N-Queens (`NQueens.java`) | ✅ Done |
| [Day 07](Day-07/) | Workflow Graphs & Conditional Edges | `workflow_graph.py` (Directed state graph, loop cycles, routers) | Trie + Backtracking — Word Search II (`WordSearchTrie.java`) | ✅ Done |
| [Day 08](Day-08/) | Agent Checkpoints & Resume | `checkpoints.py` (Atomic snapshotting, idempotency, crash resume) | Bitmask Enumeration — Subsets (`BitmaskSubsets.java`) | ✅ Done |
| [Day 09](Day-09/) | Human-in-the-Loop Approval Gates | `approval_gate.py` (Risk evaluation, approval tokens, pause/resume) | Dynamic Programming — House Robber (`HouseRobberDP.java`) | ✅ Done |
| [Day 10](Day-10/) | Parallel Tool Execution | `parallel_executor.py` (Thread pool concurrency, timeouts, failures) | 2D Grid DP — Unique Paths (`DPBottomUp.java`) | ✅ Done |
| [Day 11](Day-11/) | Multi-Tier Agent Memory Integration | `agent_memory.py` (Working, episodic, and semantic vector memory) | 0/1 Knapsack & Partition Equal Subset (`Knapsack01.java`) | ✅ Done |
| [Day 12](Day-12/) | Stopping & Budget Policies | `budget_policy.py` (Step limits, token counters, loop breaker hashes) | Dynamic Programming — Coin Change (`CoinChangeDP.java`) | ✅ Done |
| [Day 13](Day-13/) | Agent Failure Recovery | `recovery_policy.py` (Exponential backoff, tool fallback, reflection) | Longest Increasing Subsequence Patience Sort (`LongestIncreasingSubsequence.java`) | ✅ Done |
| [Day 14](Day-14/) | Agent Trajectory Evaluation | `trajectory_evaluator.py` (Tool precision, recall, step efficiency) | Dynamic Programming — Longest Common Subsequence (`LongestCommonSubsequence.java`) | ✅ Done |
| [Day 15](Day-15/) | MCP Protocol Fundamentals | `mcp_protocol_spec.py` (JSON-RPC 2.0 lifecycle, capability exchange) | 2D Dynamic Programming — Edit Distance (`EditDistance.java`) | ✅ Done |
| [Day 16](Day-16/) | Build a Basic MCP Server | `mcp_server.py` (Stdio JSON-RPC server, tools/list, tools/call) | Interval DP — Burst Balloons (`BurstBalloons.java`) | ✅ Done |
| [Day 17](Day-17/) | MCP Resources and Prompts | `mcp_resources_prompts.py` (URI-based document reads, prompt templates) | Partition DP — Matrix Chain Multiplication (`MatrixChainMultiplication.java`) | ✅ Done |
| [Day 18](Day-18/) | Build an MCP Client | `mcp_client.py` (Subprocess lifecycle, tool discovery, RPC dispatch) | Tree DP — House Robber III (`HouseRobberTree.java`) | ✅ Done |
| [Day 19](Day-19/) | Connect LLM Tool Selection to MCP | `llm_mcp_bridge.py` (Schema translation, function calling bridge) | Topological Sort + DP — Longest Path in DAG (`LongestPathInDAG.java`) | ✅ Done |
| [Day 20](Day-20/) | MCP Authentication & Authorization | `mcp_authz.py` (Bearer tokens, fine-grained scopes, RBAC) | Shortest Path — Network Delay Time Dijkstra (`NetworkDelayTime.java`) | ✅ Done |
| [Day 21](Day-21/) | MCP Security Threat Modeling | `mcp_security_audit.py` (Prompt injection, path traversal, shell jailing) | Disjoint Set Union — Accounts Merge (`AccountsMerge.java`) | ✅ Done |
| [Day 22](Day-22/) | MCP Long-Running Async Tasks | `mcp_async_tasks.py` (Background tasks, progress polling, cancellation) | Topological Sort — Parallel Courses (`ParallelCourses.java`) | ✅ Done |
| [Day 23](Day-23/) | Multi-Agent Architecture Trade-Offs | `multi_agent_system.py` (Orchestrator-Worker vs P2P, message hops) | Disjoint Set Union — Redundant Connection (`RedundantConnection.java`) | ✅ Done |
| [Day 24](Day-24/) | Agent Delegation & Result Synthesis | `agent_delegator.py` (Subtask contracts, conflict resolution) | Quickselect — Kth Largest Element (`KthLargestElement.java`) | ✅ Done |
| [Day 25](Day-25/) | Agent Sandboxing & Side-Effect Control | `agent_sandbox.py` (Filesystem allowlists, dry-run, rollback journals) | Bucket Sort — Top K Frequent Elements (`TopKFrequentElements.java`) | ✅ Done |
| [Day 26](Day-26/) | Agent Observability & Tracing | `agent_tracer.py` (OpenTelemetry spans, tokens, latency, status) | Rolling Hash — Rabin-Karp Substring Search (`RabinKarpSubstringSearch.java`) | ✅ Done |
| [Day 27](Day-27/) | Agent Regression Test Suite | `agent_regression_suite.py` (Deterministic test matrices, CI assertions) | String Matching — Knuth-Morris-Pratt (`KMPAlgorithm.java`) | ✅ Done |
| [Day 28](Day-28/) | Agent Platform System Design | `agent_system_design.py` (Task queue, worker pool, state store) | Trie + Backtracking — Word Search II (`WordSearchTwo.java`) | ✅ Done |
| [Day 29](Day-29/) | MCP Agent Integration Test | `mcp_agent_e2e.py` (End-to-end multi-turn pipeline verification) | 2D Dynamic Programming — Wildcard Matching (`WildcardMatching.java`) | ✅ Done |
| [Day 30](Day-30/) | Project 4 Release: MCP-Enabled Agent | `enterprise_mcp_agent.py` (Production release, audit trails, guards) | 90-Min Mock: Course Schedule II & Target Sum (`MockInterviewDSA.java`) | ✅ Done |
| [Day 31](Day-31/) | Enterprise Agent & MCP Benchmark | `agent_benchmark_suite.py` (Accuracy, P99 latency, cost efficiency) | Advanced Design — LRU Cache (`LRUCache.java`) | ✅ Done |

---

## 🏗️ Directory Architecture

Every day module strictly adheres to the established repository standard:
- `AI/` — **Python GenAI engines, agent loops, MCP servers, clients, and security auditors.**
- `DSA/` — **Runnable Java solutions with comprehensive `main` verification test drivers.**
- `Interview/` — **Technical Q&A deep-dives covering systems design and algorithm invariants.**
- `Notes/` — **Explanatory engineering notes detailing theory, architecture, and production trade-offs.**
- `README.md` — **Individual day guide with problem breakdown, folder layout, and run instructions.**
