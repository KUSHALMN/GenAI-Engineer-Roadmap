# 🎯 Technical Interview Questions — Day 12: IaC & Garbage Collection

### 1. What is Terraform State Drift, and how do automated pipelines remediate it?
**Answer:**
State drift occurs when cloud infrastructure is modified out-of-band (e.g., via the AWS console or manual CLI changes) so that real infrastructure diverges from the committed Terraform state file. Automated CI/CD pipelines run scheduled `terraform plan -detailed-exitcode` jobs to detect drift and either notify engineers or automatically trigger `terraform apply` to overwrite unauthorized changes.

### 2. Compare the G1 Garbage Collector with ZGC (Z Garbage Collector).
**Answer:**
- **G1 (Garbage-First):** Partitions heap into equal regions; focuses on collecting regions with the most garbage first within a target pause time budget (e.g., `-XX:MaxGCPauseMillis=200`).
- **ZGC:** Ultra-low latency collector (sub-millisecond pause times) that performs all heavy marking, reference processing, and compaction concurrently with application threads using colored pointers and load barriers.
