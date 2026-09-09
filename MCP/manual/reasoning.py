"""Manual tool-orchestration loop: prompts Ollama to emit a JSON tool call when it
needs one, executes it via the MCP client, then asks Ollama to interpret the result.

This is the same idea as ../agent.py's LangGraph ReAct agent, done by hand instead
of through a framework - useful for seeing exactly what a tool-calling loop does
under the hood, at the cost of the manual JSON convention being far less robust
than native tool-calling.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ollama import Client

import config
from mcp_client import execute_tool

PURPLE = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
SEP = "=" * 40

client = Client(host=config.OLLAMA_BASE_URL)


def _build_system_prompt(tool_info: List[Dict[str, Any]]) -> str:
    tool_descriptions = "\n\n".join(
        f"Tool: {tool['name']}\nDescription: {tool['description']}\nSchema: {json.dumps(tool['schema'], indent=2)}"
        for tool in tool_info
    )
    return f"""You are an AI assistant with access to specialized tools through MCP (Model Context Protocol).

Available tools:
{tool_descriptions}

When you need to use a tool, respond with a JSON object in the following format:
{{
    "tool": "tool_name",
    "arguments": {{
        "arg1": "value1"
    }}
}}

Do not include any other text when using a tool, just the JSON object.
For regular responses, simply respond normally.
"""


async def query_ollama(
    prompt: str,
    tool_info: List[Dict[str, Any]],
    previous_messages: Optional[List[Dict[str, str]]] = None,
) -> Tuple[str, List[Dict[str, str]]]:
    """Send a query to Ollama and process the response, executing a tool if requested."""
    if previous_messages is None:
        previous_messages = []

    print(f"{PURPLE}{SEP}")
    print("REASONING PHASE: Processing query with Ollama")
    print(f'Query: "{prompt}"')
    print(f"{SEP}{RESET}")

    system_prompt = _build_system_prompt(tool_info)

    # Ollama has no separate top-level "system" parameter like the Anthropic API;
    # the system message goes in the messages list itself, once, at the front.
    filtered_messages = [m for m in previous_messages if m["role"] != "system"]
    messages = [{"role": "system", "content": system_prompt}] + filtered_messages
    messages.append({"role": "user", "content": prompt})

    print(f"{BLUE}Sending request to Ollama...{RESET}")
    response = client.chat(model=config.OLLAMA_MODEL, messages=messages)
    ollama_response = response["message"]["content"]
    print(f"{GREEN}Received response from Ollama{RESET}")

    try:
        json_match = re.search(r"(\{[\s\S]*\})", ollama_response)
        if json_match:
            tool_request = json.loads(json_match.group(1))
            if "tool" in tool_request and "arguments" in tool_request:
                tool_name = tool_request["tool"]
                arguments = tool_request["arguments"]

                print(f"{YELLOW}Ollama wants to use tool: {tool_name}{RESET}")

                tool_result = await execute_tool(tool_name, arguments)
                if not isinstance(tool_result, str):
                    tool_result = str(tool_result)

                messages.append({"role": "assistant", "content": ollama_response})
                messages.append({"role": "user", "content": f"Tool result: {tool_result}"})

                print(f"{PURPLE}Getting Ollama's interpretation of the tool result...{RESET}")
                final_response = client.chat(model=config.OLLAMA_MODEL, messages=messages)
                final_content = final_response["message"]["content"]

                print(f"{GREEN}Final response ready{RESET}")
                print(SEP)

                messages.append({"role": "assistant", "content": final_content})
                return final_content, messages
    except (json.JSONDecodeError, KeyError, AttributeError) as e:
        print(f"{YELLOW}No tool usage detected in response: {e}{RESET}")

    print(f"{GREEN}Response ready{RESET}")
    print(SEP)

    messages.append({"role": "assistant", "content": ollama_response})
    return ollama_response, messages
