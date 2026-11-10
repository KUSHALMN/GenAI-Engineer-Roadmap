# 🎯 Technical Interview Questions — Day 11: Cloud Topology & JVM Memory

### 1. Why should GPU inference servers be placed in private subnets with NAT Gateways instead of public subnets?
**Answer:**
Placing compute instances in private subnets isolates them from unsolicited inbound internet probes and DDoS attacks. Traffic enters exclusively through public Application Load Balancers (ALB) or API gateways that terminate TLS and enforce WAF rules. Egress for model weight downloads passes through a managed NAT gateway or VPC S3 endpoint (which avoids egress fees entirely).

### 2. How does JVM Metaspace differ from the legacy PermGen space?
**Answer:**
PermGen (Java 7 and earlier) had a fixed maximum size contiguous with the Java heap, frequently causing `java.lang.OutOfMemoryError: PermGen space`. Metaspace (Java 8+) uses native OS memory to store class metadata, growing dynamically up to available OS memory (or constrained via `-XX:MaxMetaspaceSize`).
