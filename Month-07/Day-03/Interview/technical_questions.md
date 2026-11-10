# 🎯 Technical Interview Questions — Day 03: RBAC & Behavioral Patterns

### 1. Compare Role-Based Access Control (RBAC) vs. Attribute-Based Access Control (ABAC) in multi-tenant GenAI platforms.
**Answer:**
- **RBAC:** Simple, coarse-grained assignment of roles (Viewer, Editor, Admin) with static permission sets. Fast lookup and easy auditing.
- **ABAC:** Dynamic evaluation based on subject attributes (department, clearance), resource attributes (confidentiality tier, tenant_id), and environment attributes (time of day, client IP, egress gateway). In GenAI, ABAC is critical for filtering retrieved vector chunks based on document sensitivity tags and user clearance.

### 2. How does the Strategy Pattern enable zero-downtime model A/B testing?
**Answer:**
By encapsulating inference providers or reranking logic behind a unified interface (`InferenceStrategy`), runtime feature flags or routing tables can dynamically swap implementations (e.g., Llama-3-8B vs. Mistral-7B) without recompiling or redeploying the application.
