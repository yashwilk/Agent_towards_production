"""Low-level MCP client helpers: connect to the crypto MCP server over stdio,
list its tools, and invoke them directly - the raw protocol, no framework."""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import config

BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
SEP = "=" * 40


def _server_params() -> StdioServerParameters:
    return StdioServerParameters(
        command=config.PYTHON_EXECUTABLE,
        args=[config.CRYPTO_SERVER_SCRIPT],
    )


async def discover_tools() -> List[Dict[str, Any]]:
    """Connect to the MCP server and return its available tools' name/description/schema."""
    print(f"{BLUE}{SEP}\nDISCOVERY PHASE: Connecting to MCP server...{RESET}")

    async with stdio_client(_server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            print(f"{BLUE}Initializing MCP connection...{RESET}")
            await session.initialize()

            print(f"{BLUE}Discovering available tools...{RESET}")
            result = await session.list_tools()

            tool_info = [
                {"name": tool.name, "description": tool.description, "schema": tool.inputSchema}
                for tool in result.tools
            ]

    print(f"{GREEN}Successfully discovered {len(tool_info)} tools{RESET}")
    print(SEP)
    return tool_info


async def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Any:
    """Connect to the MCP server and call a single tool with the given arguments."""
    print(f"{YELLOW}{'-' * 40}")
    print(f"EXECUTION PHASE: Running tool '{tool_name}'")
    print(f"Arguments: {json.dumps(arguments, indent=2)}")
    print(f"{'-' * 40}{RESET}")

    async with stdio_client(_server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print(f"{BLUE}Sending request to MCP server...{RESET}")
            result = await session.call_tool(tool_name, arguments)

    print(f"{GREEN}Tool execution complete{RESET}")

    preview = str(result)
    if len(preview) > 150:
        preview = preview[:147] + "..."
    print(f"{BLUE}Result: {preview}{RESET}")
    print(SEP)

    return result
