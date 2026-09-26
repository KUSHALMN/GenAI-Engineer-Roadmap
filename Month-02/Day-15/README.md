# 📅 Day 45 — Month 02, Day 15: Multimodal GenAI

> Build a document/image Q&A pipeline, structured OCR text and bounding-box extraction, image token estimation, and a multimodal vision prompt flow combining text + image inputs. Implement Topological Sort for DAG dependency resolution in Python and Java.

---

## 📁 Structure

```
Day-15/
├── ocr_pipeline.py             # OCR text extraction with bounding boxes & layout classification
├── multimodal_pipeline.py      # OpenAI/Claude vision payload builder & image token estimator
├── document_qa.py              # Visual document Q&A pipeline with grounded chunk citations
├── multimodal_rag_notes.md     # Architectural guide on OCR-first vs Vision-First (ColPali) RAG
├── topological_sort.py         # Topological Sort (LC 210, Kahn's BFS & DFS, Task resolver)
├── README.md
└── DSA/
    └── TopologicalSort.java    # Topological Sort in Java (LC 210)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python ocr_pipeline.py
python multimodal_pipeline.py
python document_qa.py
python topological_sort.py
```

### Java Tests
```bash
cd DSA
javac TopologicalSort.java
java TopologicalSort
```

---

## ✅ Status: Completed
