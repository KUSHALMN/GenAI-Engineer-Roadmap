# 🎯 Technical Interview Questions — Day 15: Secrets & Low-Level Design

### 1. Why are environment variables (e.g., `process.env` / `os.environ`) considered insufficient for production secrets management?
**Answer:**
1. **Accidental Exposure:** Child processes inherit environment variables, and crash debuggers/profilers frequently dump environment variables to logs.
2. **No Dynamic Rotation:** Updating an env var requires restarting container pods.
3. **No Audit Trails:** Environment variables do not provide access logs indicating which service or credential read the secret.
*Solution:* Use HashiCorp Vault, AWS Secrets Manager, or Google Secret Manager with IAM-based short-lived access tokens and automatic rotation.

### 2. How do you approach designing a class hierarchy for an LLD interview (e.g., Parking Lot)?
**Answer:**
1. Clarify requirements & constraints (capacity, vehicle types, pricing model).
2. Define core entities & enums (`VehicleType`, `ParkingSpot`, `Ticket`).
3. Model single responsibilities: separation of ticket issuance, space allocation algorithms, and payment calculation.
4. Address concurrency: thread-safe spot reservation using mutexes or Atomic integers.
