"""The agent served by the API: a minimal stand-in for a real LLM-backed
agent, with both a synchronous and a token-streaming response mode."""

import asyncio

import config


class SimpleAgent:
    def __init__(self, name: str = config.AGENT_NAME):
        self.name = name

    def generate_response(self, query: str) -> str:
        """Generate a synchronous response to a user query."""
        return f"Agent {self.name} received: '{query}'\nResponse: This is a simulated agent response."

    async def generate_response_stream(self, query: str):
        """Generate a streaming response to a user query, one token at a time."""
        yield f"Agent {self.name} thinking about: '{query}'\n"

        response = "This is a simulated agent response that streams token by token."
        for token in response.split():
            await asyncio.sleep(0.1)  # simulate thinking time
            yield token + " "
