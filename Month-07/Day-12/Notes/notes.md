# 📝 Notes — Day 12: Infrastructure as Code & Garbage Collection

## 1. IaC Safety Principles
- Store state remotely with distributed locks (AWS S3 + DynamoDB state locking).
- Always inspect `terraform plan` output prior to applying changes.
- Enable `prevent_destroy = true` lifecycle blocks on production databases and storage buckets.
