import sys
import os

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from tool_registry import ToolRegistry
from tools.calculator import calculate
from tools.chat_history import search_chat_history, get_chat_history, save_chat_summary
from llm import ToolCallingAgent


def setup_assistant() -> ToolCallingAgent:
    """Configures the tool registry and agent."""
    registry = ToolRegistry()

    # Register tools
    registry.register(
        calculate,
        name="calculate",
        description="Safely evaluate mathematical expressions (arithmetic, sqrt, sin, cos, powers, etc.)."
    )
    registry.register(
        get_chat_history,
        name="get_chat_history",
        description="Retrieve recent session topics and conversation logs from memory."
    )
    registry.register(
        search_chat_history,
        name="search_chat_history",
        description="Search past conversations by keyword, topic, or concept query."
    )
    registry.register(
        save_chat_summary,
        name="save_chat_summary",
        description="Save a summary of the current conversation topic and key points into memory."
    )

    agent = ToolCallingAgent(registry=registry)
    return agent


def log_tool_invocation(tool_name: str, args: dict):
    print(f"\n⚙️  [TOOL INVOKED]: {tool_name}")
    print(f"   Arguments: {args}\n")


def run_demo(agent: ToolCallingAgent):
    """Runs a sequence of automated demonstration queries."""
    print("=" * 60)
    print("🤖 RUNNING AUTOMATED DEMO OF TOOL-CALLING ASSISTANT")
    print(f"Provider Active: {agent.provider.upper()}")
    print("=" * 60)

    demo_prompts = [
        "What is the result of (15 * 4) + sqrt(144) - 2^3?",
        "What did we discuss in previous sessions regarding Heap and Priority Queues?",
        "Can you calculate the square root of 625 multiplied by 4?",
        "Save a summary that today we implemented an OpenAI-compatible Tool Calling Assistant.",
    ]

    for prompt in demo_prompts:
        print(f"\n👤 User: {prompt}")
        response = agent.chat(prompt, on_tool_call=log_tool_invocation)
        print(f"🤖 Assistant:\n{response}")
        print("-" * 60)


def interactive_chat(agent: ToolCallingAgent):
    """Starts an interactive CLI session."""
    print("=" * 60)
    print("🤖 Tool-Calling AI Assistant Initialized!")
    print(f"   Provider: {agent.provider.upper()}")
    print("   Type 'exit' or 'quit' to stop.")
    print("   Type 'demo' to run automated sample queries.")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("\nGoodbye!")
                break
            if user_input.lower() == "demo":
                run_demo(agent)
                continue

            response = agent.chat(user_input, on_tool_call=log_tool_invocation)
            print(f"\nAssistant:\n{response}")

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break


def main():
    agent = setup_assistant()
    if len(sys.argv) > 1 and sys.argv[1] in ("--demo", "-d", "demo"):
        run_demo(agent)
    else:
        # Check if stdin is interactive
        if sys.stdin.isatty():
            interactive_chat(agent)
        else:
            run_demo(agent)


if __name__ == "__main__":
    main()
