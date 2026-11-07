# Day 04 Notes: Data Splitting and Leakage Prevention

## 1. Splitting Guidelines
- Always fix random seed for reproducibility (`seed=42`).
- Check pairwise hash intersections between train and test sets.
- If data has groupings (e.g. users, documents), split by group, not by random row.
