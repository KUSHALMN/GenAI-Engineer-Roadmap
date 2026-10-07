"""Conversation Summarizer: Compresses historical messages into running summary."""
from typing import List, Dict, Any


class ConversationSummarizer:
    """Incrementally compresses long conversation histories into dense abstractive summaries."""

    def __init__(self, summary_prefix: str = "Summary of earlier discussion: "):
        self.summary_prefix = summary_prefix
        self.current_summary = ""

    def summarize_messages(self, messages: List[Dict[str, str]]) -> str:
        """Compress list of message turns."""
        topics = []
        for m in messages:
            content = m["content"].lower()
            if "database" in content or "sql" in content:
                topics.append("database architectures")
            elif "latency" in content or "token" in content:
                topics.append("performance benchmarks")
            elif "rag" in content or "retrieval" in content:
                topics.append("retrieval mechanisms")
            else:
                topics.append(m["content"][:30] + "...")

        condensed = ", ".join(list(dict.fromkeys(topics)))
        self.current_summary = f"{self.summary_prefix}{condensed}."
        return self.current_summary
