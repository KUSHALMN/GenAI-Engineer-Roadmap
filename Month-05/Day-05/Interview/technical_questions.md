# Day 05: Technical Interview Preparation — Synthetic Data & Java Generics

### Q1: What is the "Model Collapse" phenomenon when training on purely synthetic LLM data?
**Answer:**
When successive generations of models are trained entirely on the outputs of prior models, rare events and tails of the statistical distribution disappear. Variance collapses, causing grammatical and stylistic degeneration, repetitive outputs, and irreversible loss of diverse knowledge.

### Q2: Explain the PECS principle in Java Generics (Producer Extends, Consumer Super).
**Answer:**
- **Producer Extends (`? extends T`):** Use when you only *read* items from a collection (it produces $T$). You cannot add new elements (except null) because the exact subtype is unknown.
- **Consumer Super (`? super T`):** Use when you only *write/add* items of type $T$ into the collection (it consumes $T$).
