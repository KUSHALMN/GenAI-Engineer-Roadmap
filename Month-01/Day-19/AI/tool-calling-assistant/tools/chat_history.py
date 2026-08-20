"""
Chat History tool for managing and searching past conversation sessions and episodic memory.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Default file location for storing session history
HISTORY_STORAGE_FILE = "conversation_history.json"


def _load_history() -> List[Dict]:
    """Loads recorded conversation logs from local storage."""
    if not os.path.exists(HISTORY_STORAGE_FILE):
        # Provide seed history for immediate demonstration
        seed_data = [
            {
                "timestamp": "2026-08-18 10:15:00",
                "session_id": "sess_001",
                "topic": "Python Generators and Iterators",
                "summary": "User learned about yield expressions, memory profiling of iterators, and custom itertools.",
                "keywords": ["python", "generators", "yield", "memory", "iterators"],
            },
            {
                "timestamp": "2026-08-19 14:30:00",
                "session_id": "sess_002",
                "topic": "Heap and Priority Queue DSA",
                "summary": "Discussed min-heap vs max-heap mechanics, Top-K elements, and Java PriorityQueue custom comparators.",
                "keywords": ["dsa", "heap", "priority queue", "top k", "java"],
            },
            {
                "timestamp": "2026-08-20 09:00:00",
                "session_id": "sess_003",
                "topic": "LLM Function Calling and Schemas",
                "summary": "Exploring OpenAI-compatible tool calling conventions, tool registration, and error handling loops.",
                "keywords": ["llm", "function calling", "tools", "schemas", "agents"],
            },
        ]
        with open(HISTORY_STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(seed_data, f, indent=2)
        return seed_data

    try:
        with open(HISTORY_STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_history(records: List[Dict]) -> None:
    """Saves conversation records to JSON file."""
    with open(HISTORY_STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def get_chat_history(limit: int = 5) -> str:
    """
    Retrieves the most recent chat session summaries from memory.

    Args:
        limit: Maximum number of recent history records to return. Defaults to 5.

    Returns:
        Formatted string containing summary of past chat sessions.
    """
    history = _load_history()
    if not history:
        return "No previous chat history found."

    recent = history[-limit:]
    formatted = []
    for item in recent:
        formatted.append(
            f"[{item.get('timestamp')}] Session: {item.get('session_id')} | "
            f"Topic: {item.get('topic')}\n"
            f"Summary: {item.get('summary')}\n"
            f"Keywords: {', '.join(item.get('keywords', []))}"
        )
    return "\n---\n".join(formatted)


def search_chat_history(query: str) -> str:
    """
    Searches past chat sessions by keyword, topic, or query string.

    Args:
        query: Keyword or phrase to search across topic, summary, or keywords.

    Returns:
        Matching conversation sessions or a message indicating no matches.
    """
    history = _load_history()
    q = query.lower()
    matches = []

    for item in history:
        topic_match = q in item.get("topic", "").lower()
        summary_match = q in item.get("summary", "").lower()
        keyword_match = any(q in k.lower() for k in item.get("keywords", []))

        if topic_match or summary_match or keyword_match:
            matches.append(
                f"• [{item.get('timestamp')}] {item.get('topic')}: {item.get('summary')}"
            )

    if not matches:
        return f"No previous conversations found matching '{query}'."

    return f"Found {len(matches)} matching conversation(s):\n" + "\n".join(matches)


def save_chat_summary(topic: str, summary: str, keywords: Optional[List[str]] = None) -> str:
    """
    Saves a summary of the current session to long-term memory.

    Args:
        topic: The primary theme or topic discussed.
        summary: A concise recap of the session's key takeaways.
        keywords: Optional list of tags or keywords for indexing.

    Returns:
        Status message confirming the record was saved.
    """
    history = _load_history()
    session_id = f"sess_{len(history) + 1:03d}"
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "session_id": session_id,
        "topic": topic,
        "summary": summary,
        "keywords": keywords or [topic.lower()],
    }
    history.append(new_entry)
    _save_history(history)
    return f"Successfully saved session summary [{session_id}] for topic: '{topic}'."
