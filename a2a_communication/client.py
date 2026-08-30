"""Reusable A2A client helpers: resolving agent cards and sending messages."""

from __future__ import annotations

import uuid

import httpx

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import AgentCard, JSONRPCErrorResponse, Message, MessageSendParams, SendMessageRequest


class A2ARequestError(RuntimeError):
    """Raised when an agent returns a JSON-RPC error response."""


async def get_agent_card(httpx_client: httpx.AsyncClient, base_url: str) -> AgentCard:
    resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
    return await resolver.get_agent_card()


async def send_text_message(base_url: str, text: str) -> str:
    """Sends a text message to the agent at base_url and returns its text reply."""
    async with httpx.AsyncClient() as httpx_client:
        agent_card = await get_agent_card(httpx_client, base_url)
        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(
                message={
                    "role": "user",
                    "messageId": str(uuid.uuid4()),
                    "parts": [{"kind": "text", "text": text}],
                }
            ),
        )
        response = await client.send_message(request)

    result = response.root
    if isinstance(result, JSONRPCErrorResponse):
        raise A2ARequestError(f"{base_url} returned error {result.error.code}: {result.error.message}")

    reply = result.result
    if not isinstance(reply, Message):
        raise A2ARequestError(f"{base_url} returned a long-running Task; this agent only expects direct replies")

    return "\n".join(part.root.text for part in reply.parts if part.root.kind == "text")
