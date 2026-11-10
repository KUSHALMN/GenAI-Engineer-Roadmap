# 🎯 Technical Interview Questions — Day 21: DR & Object Storage LLD

### 1. Contrast Recovery Point Objective (RPO) with Recovery Time Objective (RTO).
**Answer:**
- **RPO (Recovery Point Objective):** The maximum acceptable amount of data loss measured in time (e.g., RPO = 5 minutes means no more than 5 minutes of committed database transactions may be lost in a disaster).
- **RTO (Recovery Time Objective):** The maximum acceptable duration of system downtime to restore the service to operational state (e.g., RTO = 15 minutes means recovery procedures must complete within 15 minutes).

### 2. How does Write-Ahead Logging (WAL) enable Point-in-Time Recovery in PostgreSQL?
**Answer:**
PostgreSQL continuously writes changes to WAL segments before applying them to data pages. To perform PITR, an administrator restores the baseline physical file backup and replays WAL log records up to the exact designated target timestamp or transaction ID, stopping immediately prior to the accidental DROP TABLE or corruption event.
