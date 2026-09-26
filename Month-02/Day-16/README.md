# 📅 Day 46 — Month 02, Day 16: GenAI Data Engineering

> Build a text normalization and HTML cleaning pipeline, a JSONL instruction-dataset validator, exact and fuzzy Jaccard deduplicators, a batch PII scrubber, a dataset quality report generator, and a train/val splitter. Implement Union-Find (DSU) in Python and Java.

---

## 📁 Structure

```
Day-16/
├── data_cleaner.py             # HTML strip, Unicode normalization, whitespace cleaner
├── jsonl_validator.py          # Line-by-line syntax & schema validator for JSONL datasets
├── deduplicator.py             # Exact SHA-256 and fuzzy character n-gram Jaccard deduplication
├── pii_scrubber.py             # Batch PII redaction (email, phone, SSN, IP, credit cards)
├── dataset_quality_report.py   # Dataset quality reporting & reproducible train/validation splitter
├── union_find.py               # Disjoint Set Union (LC 547, LC 684) with path compression
├── README.md
└── DSA/
    └── UnionFind.java          # Union-Find in Java (LC 547, LC 684)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python data_cleaner.py
python jsonl_validator.py
python deduplicator.py
python pii_scrubber.py
python dataset_quality_report.py
python union_find.py
```

### Java Tests
```bash
cd DSA
javac UnionFind.java
java UnionFind
```

---

## ✅ Status: Completed
