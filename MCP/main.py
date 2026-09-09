"""
Ollama-powered MCP agent: a LangGraph ReAct agent, running entirely on a local
Ollama model, that answers cryptocurrency questions by calling tools exposed by
the crypto-price-tracker MCP server (server/crypto_server.py) over stdio.

No cloud LLM or API key required - tool-calling is handled locally by Ollama.
"""

import asyncio

from agent import build_agent

DEMO_QUESTIONS = [
    "What's the current price of bitcoin in usd?",
    "Give me the market info for ethereum and solana.",
]


async def run_demo(agent) -> None:
    for question in DEMO_QUESTIONS:
        result = await agent.ainvoke({"messages": [("user", question)]})
        answer = result["messages"][-1].content
        print(f"\nYou: {question}")
        print(f"Agent: {answer}")


async def main() -> None:
    agent = await build_agent()
    await run_demo(agent)


if __name__ == "__main__":
    asyncio.run(main())
