# 🎯 Technical Interview Questions — Day 20: Incident Response & Notification LLD

### 1. What are the key stages of a Blameless Postmortem following a critical production outage?
**Answer:**
1. **Executive Summary:** Incident title, severity, duration, customer impact, root cause summary.
2. **Timeline of Events:** Chronological breakdown of failure signals, engineer triage, mitigation, and recovery.
3. **Root Cause Analysis (5 Whys):** Technical failure mechanics without assigning personal blame.
4. **Action Items (Preventative Measures):** Assigned, prioritized engineering tasks to eliminate recurrence (e.g., adding circuit breakers, timeouts, runbooks).

### 2. How do you design a notification system to prevent duplicate alerts during network flapping?
**Answer:**
Implement a deduplication and alert suppression window (e.g., in Alertmanager or Redis):
Calculate an alert fingerprint (`hash(service_name + error_code + environment)`). If an alert with the same fingerprint was dispatched within the last 15 minutes, suppress duplicate SMS/pages and append to the existing incident thread.
