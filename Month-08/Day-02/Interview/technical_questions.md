# 🎯 Technical Interview Questions — Day 02: Dataset Governance & Strings

### 1. How do you handle annotator disagreement when curating golden evaluation datasets?
**Answer:**
1. **Multi-Annotator Labeling:** Assign at least 3 domain annotators per query.
2. **Inter-Annotator Agreement (Cohen's Kappa / Fleiss' Kappa):** Measure statistical consensus beyond random chance.
3. **Adjudication Panel:** Test cases with Kappa $< 0.70$ are routed to senior domain specialists to establish canonical ground truth and refine ambiguous annotation guidelines.

### 2. Why is an integer array `int[26]` more efficient than a `HashMap<Character, Integer>` for ASCII anagrams?
**Answer:**
An array of 26 primitive integers requires no object allocation, no hashing computation, and no pointer dereferencing, operating entirely within CPU L1 cache with $O(1)$ space and near-instantaneous indexing.
