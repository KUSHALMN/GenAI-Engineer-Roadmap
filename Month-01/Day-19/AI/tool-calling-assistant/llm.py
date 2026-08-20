"""
LLM Client handling tool calling orchestration loops.
Supports Groq and OpenAI providers with automatic mock simulation fallback if no API key is present.
"""

import json
import os
import uuid
from typing import Callable, Dict, Generator, List, Optional, Tuple, Any
from dotenv import load_dotenv

from schemas import ChatMessage, FunctionCall, ToolCall
from tool_registry import ToolRegistry

load_dotenv()


class ToolCallingAgent:
    """Manages multi-turn conversation and iterative function-calling cycles."""

    def __init__(
        self,
        registry: ToolRegistry,
        model: str = "llama-3.3-70b-versatile",
        system_prompt: Optional[str] = None,
        max_tool_iterations: int = 5,
    ):
        self.registry = registry
        self.model = model
        self.max_tool_iterations = max_tool_iterations
        self.system_prompt = system_prompt or (
            "You are a helpful, precise AI assistant equipped with specialized tools.\n"
            "When a user asks a question that requires calculation or querying past discussions, "
            "always call the appropriate tool. After obtaining the tool result, provide a clear, user-friendly response."
        )
        self.messages: List[ChatMessage] = [
            ChatMessage(role="system", content=self.system_prompt)
        ]
        self._init_client()

    def _init_client(self):
        """Initializes the OpenAI or Groq client."""
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        if self.groq_api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.groq_api_key)
                self.provider = "groq"
                return
            except ImportError:
                pass

        if self.openai_api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_api_key)
                self.provider = "openai"
                if "llama" in self.model:
                    self.model = "gpt-4o-mini"
                return
            except ImportError:
                pass

        # Fallback to OpenAI SDK with Groq base URL if groq package isn't installed
        if self.groq_api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=self.groq_api_key,
                )
                self.provider = "groq-openai-compat"
                return
            except ImportError:
                pass

        self.provider = "mock"

    def _mock_llm_response(self, user_text: str) -> Tuple[Optional[str], Optional[List[ToolCall]]]:
        """Heuristic mock response when no API key is provided (for demo/testing)."""
        lower = user_text.lower()

        # Check for save summary requests
        if "save" in lower and "summary" in lower:
            tool_id = f"call_{uuid.uuid4().hex[:8]}"
            tc = ToolCall(
                id=tool_id,
                function=FunctionCall(
                    name="save_chat_summary",
                    arguments=json.dumps({
                        "topic": "LLM Tool Calling Assistant",
                        "summary": "Implemented dynamic schema generation, OpenAI tool calling loop, and safe execution tools.",
                        "keywords": ["tool calling", "agents", "openai", "schemas"],
                    }),
                ),
            )
            return None, [tc]

        # Check for history search requests
        if any(w in lower for w in ["history", "previous", "recall", "past session", "yesterday", "topics", "discuss"]):
            tool_id = f"call_{uuid.uuid4().hex[:8]}"
            if "search" in lower or "find" in lower:
                query = lower.replace("search", "").replace("history", "").replace("for", "").strip()
                tc = ToolCall(
                    id=tool_id,
                    function=FunctionCall(name="search_chat_history", arguments=json.dumps({"query": query or "heap"})),
                )
            else:
                tc = ToolCall(
                    id=tool_id,
                    function=FunctionCall(name="get_chat_history", arguments=json.dumps({"limit": 3})),
                )
            return None, [tc]

        # Check for calculation requests
        if any(w in lower for w in ["calculate", "math", "+", "-", "*", "/", "sqrt", "sin", "cos", "^", "result"]):
            # Extract clean mathematical expression
            expr = user_text
            if "result of" in lower:
                expr = user_text[lower.find("result of") + 9:].strip(" ?:!.")
            elif "calculate" in lower:
                expr = user_text[lower.find("calculate") + 9:].strip(" ?:!.")
            elif "compute" in lower:
                expr = user_text[lower.find("compute") + 7:].strip(" ?:!.")

            # Simple conversion of word expressions for mock demo
            expr = expr.replace("the square root of 625 multiplied by 4", "sqrt(625) * 4")
            tool_id = f"call_{uuid.uuid4().hex[:8]}"
            tc = ToolCall(
                id=tool_id,
                function=FunctionCall(name="calculate", arguments=json.dumps({"expression": expr or "25 * 4 + 10"})),
            )
            return None, [tc]

        return (
            f"[Mock LLM Response] I received your prompt: '{user_text}'. (Provide a GROQ_API_KEY or OPENAI_API_KEY in .env for live LLM completions).",
            None,
        )

    def chat(self, user_input: str, on_tool_call: Optional[Callable[[str, Dict], None]] = None) -> str:
        """
        Executes a complete chat turn with autonomous tool-calling resolution.
        """
        self.messages.append(ChatMessage(role="user", content=user_input))
        tools_schema = self.registry.get_tools_schema()

        iteration = 0
        while iteration < self.max_tool_iterations:
            iteration += 1

            if self.provider == "mock":
                # Simulated iteration
                if self.messages[-1].role == "tool":
                    # Assistant summarizes tool result
                    tool_res = self.messages[-1].content
                    final_text = f"[Simulation] Result from tool was: {tool_res}\nBased on this, here is your answer."
                    self.messages.append(ChatMessage(role="assistant", content=final_text))
                    return final_text

                text, tool_calls = self._mock_llm_response(user_input)
                if tool_calls:
                    self.messages.append(ChatMessage(role="assistant", tool_calls=tool_calls))
                    for tc in tool_calls:
                        if on_tool_call:
                            on_tool_call(tc.function.name, json.loads(tc.function.arguments))
                        exec_res = self.registry.execute(tc.id, tc.function.name, tc.function.arguments)
                        self.messages.append(exec_res.to_tool_message())
                    continue
                else:
                    self.messages.append(ChatMessage(role="assistant", content=text))
                    return text or ""

            # Real API invocation
            try:
                formatted_messages = [msg.to_dict() for msg in self.messages]
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=formatted_messages,
                    tools=tools_schema if tools_schema else None,
                    tool_choice="auto" if tools_schema else None,
                    temperature=0.2,
                )

                choice = response.choices[0]
                message = choice.message

                # Check if model made tool calls
                if message.tool_calls:
                    parsed_tool_calls = []
                    for tc in message.tool_calls:
                        parsed_tool_calls.append(
                            ToolCall(
                                id=tc.id,
                                function=FunctionCall(
                                    name=tc.function.name,
                                    arguments=tc.function.arguments,
                                ),
                            )
                        )

                    self.messages.append(
                        ChatMessage(
                            role="assistant",
                            content=message.content,
                            tool_calls=parsed_tool_calls,
                        )
                    )

                    # Execute each tool call
                    for tc in parsed_tool_calls:
                        if on_tool_call:
                            try:
                                args_dict = json.loads(tc.function.arguments)
                            except Exception:
                                args_dict = {"raw": tc.function.arguments}
                            on_tool_call(tc.function.name, args_dict)

                        exec_result = self.registry.execute(
                            tool_call_id=tc.id,
                            function_name=tc.function.name,
                            arguments_str=tc.function.arguments,
                        )
                        self.messages.append(exec_result.to_tool_message())

                    # Loop again so the LLM gets the tool output and can formulate final reply or call another tool
                    continue

                else:
                    final_content = message.content or ""
                    self.messages.append(ChatMessage(role="assistant", content=final_content))
                    return final_content

            except Exception as e:
                err_msg = f"LLM API Error ({self.provider}): {str(e)}"
                self.messages.append(ChatMessage(role="assistant", content=err_msg))
                return err_msg

        return "Maximum tool iterations reached without concluding a response."
