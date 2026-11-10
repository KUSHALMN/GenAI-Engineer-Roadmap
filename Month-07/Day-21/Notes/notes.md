# 📝 Notes — Day 21: Disaster Recovery & Object Storage

## 1. High-Availability Backup Strategy
- **Base Backups:** Daily full pg_basebackup uploaded to multi-region object storage.
- **Continuous WAL Archiving:** Every 16MB WAL segment archived immediately to S3 with object locking (WORM: Write Once Read Many).
