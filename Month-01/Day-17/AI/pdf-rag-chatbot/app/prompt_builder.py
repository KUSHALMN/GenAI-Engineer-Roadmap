from __future__ import annotations

from typing import List


def build_rag_prompt(
    question: str, context_chunks: List[str], system_instruction: str | None = None
) -> str:
    """Construct a grounded prompt for the LLM using retrieved context passages."""
    system_part = (
        system_instruction
        or "You are a helpful and accurate AI assistant. Answer the user's question ONLY using the provided context. If the context does not contain enough information to answer, state 'I cannot answer this based on the provided document.'"
    )

    formatted_context = "\n\n---\n\n".join(
        f"[Context Snippet {i+1}]:\n{chunk}" for i, chunk in enumerate(context_chunks)
    )

    prompt = f"""{system_part}

=== CONTEXT PASSAGES ===
{formatted_context if formatted_context else "No context available."}
========================

User Question: {question}

Helpful Answer:"""

    return prompt
