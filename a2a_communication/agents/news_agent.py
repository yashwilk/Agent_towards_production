"""News Information Agent: provides the news snippet of the daily TLDR."""

from __future__ import annotations

import os
from typing import Optional

from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from starlette.applications import Starlette

from agents.common import SimpleTextAgentExecutor, build_app

AGENT_NAME = "News Information Agent"
BASE_URL = os.getenv("NEWS_AGENT_BASE_URL", "http://localhost:9001")


async def get_latest_news(query: Optional[str] = None) -> str:
    # Placeholder for real logic (news API, RAG lookup, etc.).
    return "Breaking News: AI discovers a new way to make coffee!"


def build_agent_card() -> AgentCard:
    return AgentCard(
        name=AGENT_NAME,
        description="Provides news headlines for the TLDR of the day.",
        url=BASE_URL,
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(
                id="get_latest_news",
                name="Get Latest News",
                description="Provides the latest news headline.",
                tags=["news", "information", "tldr"],
                examples=["what is the news?", "latest headline", "give me news"],
            )
        ],
        supportsAuthenticatedExtendedCard=False,
    )


def create_app() -> Starlette:
    executor = SimpleTextAgentExecutor(AGENT_NAME, get_latest_news)
    return build_app(build_agent_card(), executor)
