"""Demo verifying Model Context Protocol (MCP) server-client lifecycle."""
import sys
import os

# Ensure Day-30 root is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server import MCPServer
from mcp.client import MCPClient


def run_demo():
    print("==================================================")
    print(" Day 30: Model Context Protocol (MCP) Full Demo")
    print("==================================================")

    server = MCPServer("cloud-mcp-cluster")
    client = MCPClient(server)

    # 1. Discover tools
    tools = client.list_tools()
    print(f"\n[1] Discovered {len(tools)} MCP Tools:")
    for t in tools:
        print(f"    - {t['name']}: {t['description']}")

    # 2. Invoke arithmetic tool
    calc_res = client.call_tool("calculate_expression", {"expression": "(45 * 12) + 160"})
    print(f"\n[2] Executed 'calculate_expression':")
    print(f"    Output -> {calc_res['result']}")
    assert calc_res["result"] == 700

    # 3. Invoke text statistics tool
    sample_text = "Model Context Protocol standardizes AI integrations across enterprise data systems."
    stats_res = client.call_tool("text_statistics", {"text": sample_text})
    print(f"\n[3] Executed 'text_statistics':")
    print(f"    Word count -> {stats_res['word_count']}, Char count -> {stats_res['character_count']}")

    # 4. Read resources
    resources = client.list_resources()
    print(f"\n[4] Discovered {len(resources)} Resources:")
    for r in resources:
        print(f"    - {r['uri']} ({r['name']})")

    policy_content = client.read_resource("docs://company/policy")
    print(f"\n[5] Read 'docs://company/policy':")
    print(f"    Content: '{policy_content}'")

    print("\nMCP Protocol Client/Server execution completed successfully! [OK]")


if __name__ == "__main__":
    run_demo()
