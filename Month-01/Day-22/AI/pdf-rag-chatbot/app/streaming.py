import asyncio
import json
import time
from typing import AsyncGenerator, Dict, Any
from app.rag_pipeline import RAGPipeline
from app.config import settings

class StreamingRAGService:
    """
    Service to stream RAG responses via Server-Sent Events (SSE) protocol.
    Emits token events, citation metadata, and completion indicators.
    """

    @staticmethod
    async def stream_query(pipeline: RAGPipeline, query: str, top_k: int = 4) -> AsyncGenerator[str, None]:
        """
        Generate SSE chunks for a given user query.
        Event stream format:
          data: {"type": "metadata", "citations": [...], "retrieved_count": N}
          data: {"type": "token", "content": "..."}
          data: {"type": "done", "total_latency_ms": X, "ttft_ms": Y}
        """
        start_time = time.time()
        ttft_recorded = False
        ttft_ms = 0.0

        # Retrieve relevant chunks
        retrieved_chunks = pipeline.retriever.retrieve(query, top_k=top_k)

        citations = []
        context_blocks = []
        for idx, chunk in enumerate(retrieved_chunks):
            source = chunk.get("source", "doc")
            page = chunk.get("page_number", 1)
            cid = chunk.get("chunk_id", f"c_{idx}")
            context_blocks.append(f"[{idx+1}] (Source: {source}, Page: {page})\n{chunk['text']}")
            citations.append({
                "source": source,
                "page": page,
                "chunk_id": cid,
                "score": chunk.get("hybrid_rrf_score", 0.0),
                "snippet": chunk["text"][:150]
            })

        # Yield metadata event
        meta_event = {
            "type": "metadata",
            "citations": citations,
            "retrieved_count": len(retrieved_chunks)
        }
        yield f"data: {json.dumps(meta_event)}\n\n"

        context_str = "\n\n".join(context_blocks) if context_blocks else "No relevant documents found."
        
        # Check LLM streaming provider
        if settings.LLM_PROVIDER.lower() == "groq" and settings.GROQ_API_KEY:
            try:
                from groq import AsyncGroq
                client = AsyncGroq(api_key=settings.GROQ_API_KEY)
                system_prompt = (
                    "You are a precise, helpful AI PDF Assistant. Answer strictly based on the provided context."
                )
                response_stream = await client.chat.completions.create(
                    model=settings.LLM_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"}
                    ],
                    temperature=settings.TEMPERATURE,
                    max_tokens=settings.MAX_TOKENS,
                    stream=True
                )
                async for chunk in response_stream:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        if not ttft_recorded:
                            ttft_ms = round((time.time() - start_time) * 1000, 2)
                            ttft_recorded = True
                        token_event = {"type": "token", "content": delta}
                        yield f"data: {json.dumps(token_event)}\n\n"
            except Exception as e:
                # Fallback to simulated token stream
                pass

        # Simulated Streaming Fallback
        full_answer = pipeline._generate_response(query, context_str)
        words = full_answer.split(" ")

        for idx, word in enumerate(words):
            if not ttft_recorded:
                ttft_ms = round((time.time() - start_time) * 1000, 2)
                ttft_recorded = True

            token_chunk = word + (" " if idx < len(words) - 1 else "")
            token_event = {"type": "token", "content": token_chunk}
            yield f"data: {json.dumps(token_event)}\n\n"
            
            # Non-blocking pause for smooth UI rendering
            await asyncio.sleep(settings.STREAM_CHUNK_DELAY_MS / 1000.0)

        total_latency_ms = round((time.time() - start_time) * 1000, 2)
        done_event = {
            "type": "done",
            "total_latency_ms": total_latency_ms,
            "ttft_ms": ttft_ms
        }
        yield f"data: {json.dumps(done_event)}\n\n"
