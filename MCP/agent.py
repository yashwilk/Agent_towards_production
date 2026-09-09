"""Builds a LangGraph ReAct agent, backed by a local Ollama model, that can call
tools exposed by the crypto-price-tracker MCP server (server/crypto_server.py)."""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

import config


def build_mcp_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "crypto": {
                "transport": "stdio",
                "command": config.PYTHON_EXECUTABLE,
                "args": [config.CRYPTO_SERVER_SCRIPT],
            }
        }
    )


async def build_agent():
    """Connect to the MCP server, load its tools, and wire them to an Ollama-backed agent."""
    client = build_mcp_client()
    tools = await client.get_tools()

    model = ChatOllama(model=config.OLLAMA_MODEL, base_url=config.OLLAMA_BASE_URL, temperature=0)
    return create_react_agent(model, tools)
