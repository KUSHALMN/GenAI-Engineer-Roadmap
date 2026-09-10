from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

from app.config import settings
from app.loader import Document, load_pdf, load_text_file
from app.prompt_builder import build_rag_prompt
from app.source_handler import format_sources
from app.splitter import RecursiveCharacterTextSplitter
from retrieval.hybrid_retriever import HYBRID_RETRIEVER
from retrieval.keyword_retriever import KEYWORD_RETRIEVER
from retrieval.reranker import RERANKER
from retrieval.semantic_retriever import SEMANTIC_RETRIEVER


class RAGPipeline:
    """End-to-End PDF RAG Pipeline."""

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.semantic_retriever = SEMANTIC_RETRIEVER
        self.keyword_retriever = KEYWORD_RETRIEVER
        self.hybrid_retriever = HYBRID_RETRIEVER
        self.reranker = RERANKER
        self.indexed_documents: List[Document] = []

    def ingest_file(self, file_path: str | Path) -> Dict[str, Any]:
        """Load, chunk, and index a PDF or text file."""
        path = Path(file_path)
        if path.suffix.lower() == ".pdf":
            raw_docs = load_pdf(path)
        else:
            raw_docs = load_text_file(path)

        chunks = self.splitter.split_documents(raw_docs)
        self.indexed_documents.extend(chunks)

        # Index across all retrieval systems
        self.semantic_retriever.index(chunks)
        self.keyword_retriever.index(chunks)
        self.hybrid_retriever.index(chunks)

        return {
            "file": path.name,
            "raw_pages_loaded": len(raw_docs),
            "chunks_created": len(chunks),
            "total_indexed_chunks": len(self.indexed_documents),
        }

    def ingest_raw_text(self, text: str, source_name: str = "manual_input") -> Dict[str, Any]:
        """Chunk and index direct text."""
        doc = Document(text=text, metadata={"source": source_name, "page": 1})
        chunks = self.splitter.split_documents([doc])
        self.indexed_documents.extend(chunks)

        self.semantic_retriever.index(chunks)
        self.keyword_retriever.index(chunks)
        self.hybrid_retriever.index(chunks)

        return {"chunks_created": len(chunks), "total_indexed_chunks": len(self.indexed_documents)}

    def retrieve_context(
        self,
        query: str,
        retriever_type: str = "hybrid",
        top_k: int = 4,
        use_reranker: bool = True,
    ) -> List[Dict[str, Any]]:
        """Retrieve and optionally rerank relevant context documents."""
        initial_k = top_k * 2 if use_reranker else top_k

        if retriever_type == "semantic":
            docs = self.semantic_retriever.retrieve(query, top_k=initial_k)
        elif retriever_type == "keyword":
            docs = self.keyword_retriever.retrieve(query, top_k=initial_k)
        else:
            docs = self.hybrid_retriever.retrieve(query, top_k=initial_k)

        if use_reranker and docs:
            docs = self.reranker.rerank(query, docs, top_k=top_k)
        else:
            docs = docs[:top_k]

        return docs

    def generate_llm_response(self, prompt: str) -> str:
        """Invoke Groq LLM API or provide deterministic fallback response."""
        api_key = settings.GROQ_API_KEY
        if api_key:
            try:
                from groq import Groq

                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model=settings.CHAT_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=1024,
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                return f"[LLM Generation Fallback (API error: {e})]\nBased on retrieved context:\n{prompt.split('=== CONTEXT PASSAGES ===')[-1][:300]}"

        # Fallback when no API key provided
        return "Based on the provided context, the information directly addresses your query with the retrieved snippets."

    def query(
        self,
        question: str,
        retriever_type: str = "hybrid",
        top_k: int = 4,
        use_reranker: bool = True,
    ) -> Dict[str, Any]:
        """Execute end-to-end question answering pipeline."""
        retrieved_docs = self.retrieve_context(
            query=question,
            retriever_type=retriever_type,
            top_k=top_k,
            use_reranker=use_reranker,
        )
        context_texts = [d.get("text", "") for d in retrieved_docs]
        prompt = build_rag_prompt(question, context_texts)
        answer = self.generate_llm_response(prompt)
        sources = format_sources(retrieved_docs)

        return {
            "question": question,
            "answer": answer,
            "retriever_type": retriever_type,
            "reranked": use_reranker,
            "retrieved_count": len(retrieved_docs),
            "sources": sources,
        }

    def clear(self) -> None:
        """Reset all indices."""
        self.indexed_documents.clear()
        self.semantic_retriever.clear()
        self.keyword_retriever.clear()
        self.hybrid_retriever.clear()


# Default singleton instance
pipeline = RAGPipeline()


def answer_question(context: str, question: str) -> str:
    """Simple baseline functional wrapper."""
    if context:
        pipeline.ingest_raw_text(context, source_name="context_snippet")
    res = pipeline.query(question=question)
    return res["answer"]
