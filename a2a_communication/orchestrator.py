"""Combines replies from the News and Events agents into one daily TLDR.

UserFacingAgent (this module): responsible for interacting with the user. It
orchestrates the task of gathering TLDR information.
NewsInfoAgent (agents/news_agent.py): specializes in providing the
news-related part of the TLDR.
EventsInfoAgent (agents/events_agent.py): specializes in providing
information about current events for the TLDR.

This orchestrator sends real A2A tasks/send requests to the NewsInfoAgent and
EventsInfoAgent over HTTP. Those agents process the requests and return their
respective TLDR snippets as A2A Task/Message responses, which are then
compiled here into the complete TLDR.
"""

from __future__ import annotations

import asyncio
import logging

from agents.events_agent import BASE_URL as EVENTS_AGENT_BASE_URL
from agents.news_agent import BASE_URL as NEWS_AGENT_BASE_URL
from client import send_text_message

logger = logging.getLogger(__name__)

NEWS_QUERY = "Please provide the news TLDR part for today."
EVENTS_QUERY = "Please provide the events TLDR part for today."


async def _fetch(base_url: str, query: str, label: str) -> str:
    try:
        return await send_text_message(base_url, query)
    except Exception:
        logger.exception("Could not get %s content from %s", label, base_url)
        return f"No {label} content available right now."


async def get_daily_tldr() -> str:
    """Queries the News and Events agents concurrently and formats a combined TLDR."""
    news_content, events_content = await asyncio.gather(
        _fetch(NEWS_AGENT_BASE_URL, NEWS_QUERY, "news"),
        _fetch(EVENTS_AGENT_BASE_URL, EVENTS_QUERY, "events"),
    )
    return (
        "Today's TLDR\n"
        "------------\n"
        f"News:\n{news_content}\n\n"
        f"Events:\n{events_content}\n"
        "------------"
    )
