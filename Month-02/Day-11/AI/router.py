"""
Request Router.
Routes queries to the appropriate handler:
- DETERMINISTIC_WORKFLOW: formatting, calculation, schema validation
- RAG_PIPELINE: information retrieval, knowledge base questions
- AUTONOMOUS_AGENT: multi-step research, tool chaining, open-ended tasks
"""

from enum import Enum
from typing import Any, Callable, Dict, Optional


class RouteDestination(str, Enum):
    DETERMINISTIC_WORKFLOW = "workflow"
    RAG_PIPELINE = "rag"
    AUTONOMOUS_AGENT = "agent"


class IntentRouter:
    """Classifies user intent and delegates to specialized processors."""

    WORKFLOW_KEYWORDS = ["format", "clean", "extract json", "calculate", "schema", "validate"]
    RAG_KEYWORDS = ["what is", "who is", "explain", "policy", "documentation", "how does"]
    AGENT_KEYWORDS = ["search and summarize", "investigate", "compare and fix", "plan and execute", "browse"]

    @classmethod
    def route_query(cls, query: str) -> RouteDestination:
        """Classify route based on semantic intent rules."""
        q_lower = query.lower()

        # Check for multi-step agent triggers first
        if any(kw in q_lower for kw in cls.AGENT_KEYWORDS) or "and then" in q_lower:
            return RouteDestination.AUTONOMOUS_AGENT

        # Check for deterministic workflow triggers
        if any(kw in q_lower for kw in cls.WORKFLOW_KEYWORDS):
            return RouteDestination.DETERMINISTIC_WORKFLOW

        # Check for knowledge query triggers
        if any(kw in q_lower for kw in cls.RAG_KEYWORDS):
            return RouteDestination.RAG_PIPELINE

        # Default to agent for general open-ended queries
        return RouteDestination.AUTONOMOUS_AGENT

    def __init__(self):
        self.handlers: Dict[RouteDestination, Callable[[str], Any]] = {}

    def register_handler(self, destination: RouteDestination, handler: Callable[[str], Any]) -> None:
        """Register destination handler."""
        self.handlers[destination] = handler

    def dispatch(self, query: str) -> Dict[str, Any]:
        """Classify and dispatch query to handler."""
        dest = self.route_query(query)
        handler = self.handlers.get(dest)

        if not handler:
            return {
                "query": query,
                "destination": dest.value,
                "result": f"No handler registered for destination: {dest.value}",
            }

        result = handler(query)
        return {
            "query": query,
            "destination": dest.value,
            "result": result,
        }


if __name__ == "__main__":
    router = IntentRouter()
    router.register_handler(RouteDestination.DETERMINISTIC_WORKFLOW, lambda q: f"Workflow executed for: {q}")
    router.register_handler(RouteDestination.RAG_PIPELINE, lambda q: f"RAG search executed for: {q}")
    router.register_handler(RouteDestination.AUTONOMOUS_AGENT, lambda q: f"Agent executed for: {q}")

    assert router.route_query("Please clean and format this raw data") == RouteDestination.DETERMINISTIC_WORKFLOW
    assert router.route_query("What is the refund policy for annual subscriptions?") == RouteDestination.RAG_PIPELINE
    assert router.route_query("Search and summarize top 3 market competitors and then compare them") == RouteDestination.AUTONOMOUS_AGENT

    res = router.dispatch("What is our security SLA?")
    print("Dispatch result:", res)
    assert res["destination"] == "rag"
    print("IntentRouter tests passed successfully!")
