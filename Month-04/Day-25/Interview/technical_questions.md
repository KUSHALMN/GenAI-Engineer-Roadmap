# Day 25: Technical Interview Preparation — Sandboxing & Bucket Sort

### Q1: Why is a Dry-Run simulation mode vital for destructive agent tools?
**Answer:**
A dry-run mode allows the agent to evaluate the downstream consequences of an action (e.g. how many database records will be deleted, or what files will be overwritten) without actually committing the mutation. The simulation results can be presented to the user or human-in-the-loop gate for explicit sign-off.

### Q2: Why is Bucket Sort $O(n)$ for Top K Frequent Elements while Heap is $O(n \log k)$?
**Answer:**
The maximum possible frequency of any element in an array of size $n$ is bounded by $n$. We can allocate an array of buckets of size $n+1$, where bucket $f$ holds all elements with frequency $f$. Inserting elements takes $O(n)$ time, and scanning buckets from $n$ down to $0$ takes $O(n)$, beating the $O(n \log k)$ heap approach.
