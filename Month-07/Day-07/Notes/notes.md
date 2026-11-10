# 📝 Notes — Day 07: Object Storage & Transaction Isolation

## 1. Cloud Storage Architecture
- **S3 Multipart Upload:** Files > 100MB should be split into 5MB-5GB parts and uploaded in parallel with automatic retries for failed parts.
- **Object Lifecycle Policies:** Transition objects from Standard -> Infrequent Access (IA) after 30 days -> Glacier Deep Archive after 90 days.
