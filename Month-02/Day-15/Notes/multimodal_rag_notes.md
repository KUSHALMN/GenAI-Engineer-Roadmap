# 👁️ Multimodal GenAI & Document RAG Notes

## 1. OCR-First vs Vision-First RAG

| Dimension | OCR-First Pipeline (Tesseract / Textract) | Vision-First Pipeline (ColPali / Vision Embeddings) |
|---|---|---|
| **Approach** | Extract text from PDF/image $\rightarrow$ standard text chunking $\rightarrow$ text embedding | Embed page screenshot directly using multi-vector vision encoders |
| **Table / Chart Understanding** | Poor: loses spatial layout, 2D coordinates, table hierarchies | Superior: visual attention naturally reads 2D layouts and graphs |
| **Indexing Cost** | High OCR compute upfront, cheap vector storage | Heavy visual embeddings (ColBERT-style multi-vector storage) |
| **Query Latency** | Low (standard dense retrieval) | Moderate (Late interaction scoring across 1024 patch vectors per page) |
| **Best For** | Plain text documents, legal contracts | Financial reports with tables, engineering schematics, slides |

---

## 2. Token Economics of Multimodal Vision Models

- **Tile-based Patching**:
  Modern vision models (e.g. GPT-4o, Claude 3.5 Sonnet) partition images into $512 \times 512$ pixel patches.
  $$\text{Tokens} = 85 + (170 \times \text{Tiles})$$
  - A $1024 \times 768$ page requires 4 tiles: $85 + (170 \times 4) = 765\text{ tokens}$.
  - A 20-page PDF rendered visually consumes $\approx 15,300\text{ prompt tokens}$ on ingestion.
- **Cost Optimization Tip**:
  Downscale documents to standard readable DPI (150–200 DPI) before sending to multimodal endpoints.
