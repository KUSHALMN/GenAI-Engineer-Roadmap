"""
Day 19: Connect LLM Tool Selection to MCP
Converts MCP tool schemas into OpenAI / Anthropic function calling format,
translates model function calls, and routes execution back to the MCP client.
"""

from typing import Dict, Any, List
import json

class LLMMCPBridge:
    @staticmethod
    def mcp_to_openai_tools(mcp_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Converts MCP tool definitions to standard OpenAI function schemas."""
        openai_tools = []
        for t in mcp_tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "parameters": t.get("inputSchema", {"type": "object", "properties": {}})
                }
            })
        return openai_tools

    @staticmethod
    def execute_llm_tool_call(llm_call: Dict[str, Any], mcp_client) -> Dict[str, Any]:
        """Parses model function call and dispatches to MCP client."""
        fn_name = llm_call["function"]["name"]
        args = json.loads(llm_call["function"]["arguments"])
        output = mcp_client.call_tool(fn_name, args)
        return {
            "tool_call_id": llm_call.get("id", "call_default"),
            "role": "tool",
            "name": fn_name,
            "content": str(output)
        }

if __name__ == "__main__":
    sample_mcp_tools = [{
        "name": "lookup_user",
        "description": "Fetch user by ID",
        "inputSchema": {
            "type": "object",
            "properties": {"user_id": {"type": "integer"}},
            "required": ["user_id"]
        }
    }]

    converted = LLMMCPBridge.mcp_to_openai_tools(sample_mcp_tools)
    assert converted[0]["type"] == "function"
    assert converted[0]["function"]["name"] == "lookup_user"

    class DummyClient:
        def call_tool(self, name, args):
            return f"User details for ID {args['user_id']}"

    mock_llm_call = {
        "id": "call_123",
        "function": {
            "name": "lookup_user",
            "arguments": json.dumps({"user_id": 42})
        }
    }
    tool_msg = LLMMCPBridge.execute_llm_tool_call(mock_llm_call, DummyClient())
    assert tool_msg["role"] == "tool"
    assert "ID 42" in tool_msg["content"]
    print("LLM-to-MCP Bridge output:")
    print(json.dumps(tool_msg, indent=2))
    print("Day 19 AI LLM-MCP Bridge passed all tests.")
