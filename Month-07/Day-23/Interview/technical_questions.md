# 🎯 Technical Interview Questions — Day 23: Provider Adapters & Testing

### 1. Why should enterprise AI platforms avoid vendor lock-in with a single LLM provider?
**Answer:**
1. **Outage Resilience:** Single provider outages (e.g., OpenAI API 503 spikes) instantly take down production apps without automatic fallback.
2. **Commercial Leverage:** The ability to route requests to whichever model offers the best cost/performance ratio (e.g., DeepSeek vs GPT-4o-mini).
3. **Data Sovereignty:** Enterprise European clients may require running on local open-weights servers (vLLM on EU cloud) rather than sending data to US API endpoints.

### 2. How do Unit Tests differ from Integration Tests and Smoke Tests in backend systems?
**Answer:**
- **Unit Tests:** Test individual classes/functions in total isolation using fast in-memory mocks. Run in milliseconds.
- **Integration Tests:** Test interactions between multiple modules or real infrastructure components (e.g., FastAPI + real PostgreSQL test container).
- **Smoke Tests:** Minimal sanity checks run against live staging/production environments post-deployment to verify core paths (health checks, login).
