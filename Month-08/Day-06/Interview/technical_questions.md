# 🎯 Technical Interview Questions — Day 06: Agent Metrics & Binary Search

### 1. How do you quantify agent trajectory efficiency beyond simple task completion?
**Answer:**
- **Step Efficiency:** Ratio of actual tool calls to the minimal required path.
- **Redundant Tool Call Rate:** Identifying duplicate calls with identical arguments.
- **Tool Call Precision & Recall:** Proportion of triggered tools that were necessary vs. hallucinated tools.
- **Self-Correction Success Rate:** Did the agent recover when a tool returned a 400 error, or did it enter an infinite loop?

### 2. Explain how to determine which half is sorted in LC 33 Search in Rotated Sorted Array.
**Answer:**
Compare `nums[left]` with `nums[mid]`:
- If `nums[left] <= nums[mid]`, the entire left half is strictly sorted. Check if target lies within `[nums[left], nums[mid])`.
- If `nums[left] > nums[mid]`, the pivot lies in the left half, meaning the right half `[nums[mid], nums[right]]` is strictly sorted. Check if target lies within `(nums[mid], nums[right]]`.
