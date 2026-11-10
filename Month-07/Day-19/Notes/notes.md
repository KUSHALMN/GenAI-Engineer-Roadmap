# 📝 Notes — Day 19: SLIs, Error Budgets & Task Scheduling

## 1. Multi-Window Multi-Burn-Rate Alerting
- Avoid alerting on raw single-minute spikes (causes alert fatigue).
- Trigger pager alerts only when 1-hour and 6-hour burn rates both exceed thresholds simultaneously.
