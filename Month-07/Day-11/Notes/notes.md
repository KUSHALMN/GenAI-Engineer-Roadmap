# 📝 Notes — Day 11: Cloud Topology & JVM Memory Architecture

## 1. Multi-AZ Cloud Architecture
- Deploy inference workers across at least two Availability Zones (AZs) behind an Application Load Balancer (ALB).
- Use VPC peering or VPC PrivateLink for zero-egress cost database and vector store communication.
