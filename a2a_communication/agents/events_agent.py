"""Current Events Information Agent: provides the events snippet of the daily TLDR."""

from __future__ import annotations

import os
from typing import Optional

from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from starlette.applications import Starlette

from agents.common import SimpleTextAgentExecutor, build_app

AGENT_NAME = "Current Events Information Agent"
BASE_URL = os.getenv("EVENTS_AGENT_BASE_URL", "http://localhost:9002")


async def get_current_events(query: Optional[str] = None) -> str:
    # Placeholder for real logic (events API, RAG lookup, etc.).
    return "Current Event: The annual 'Innovate AI' conference is happening this week!"


def build_agent_card() -> AgentCard:
    return AgentCard(
        name=AGENT_NAME,
        description="Provides updates on current events for the TLDR of the day.",
        url=BASE_URL,
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(
                id="get_current_events",
                name="Get Current Events",
                description="Provides information about current events.",
                tags=["events", "information", "tldr", "conference"],
                examples=["what are the current events?", "any ongoing events?", "tell me about events"],
            )
        ],
        supportsAuthenticatedExtendedCard=False,
    )


def create_app() -> Starlette:
    executor = SimpleTextAgentExecutor(AGENT_NAME, get_current_events)
    return build_app(build_agent_card(), executor)
