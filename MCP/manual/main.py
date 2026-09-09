"""
Manual MCP + Ollama example: the same crypto-price-tracker MCP server as ../main.py's
LangGraph agent, but wired up by hand - explicit tool discovery, a JSON-based
tool-call convention prompted into the system message, and a manual execute-then-
reinterpret loop - to show what a framework like LangGraph is doing under the hood.
"""

import asyncio

from mcp_client import discover_tools
from reasoning import query_ollama

DEMO_QUESTIONS = [
    "What's the current price of bitcoin in usd?",
    "Give me the market info for ethereum and solana.",
]


async def main() -> None:
    tools = await discover_tools()
    print(f"Discovered {len(tools)} tools:")
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}: {tool['description']}")

    messages = None
    for question in DEMO_QUESTIONS:
        answer, messages = await query_ollama(question, tools, previous_messages=messages)
        print(f"\nYou: {question}")
        print(f"Assistant: {answer}")


if __name__ == "__main__":
    asyncio.run(main())
