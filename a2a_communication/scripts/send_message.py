"""CLI to send a text message to one of the running agents.

Usage:
    python send_message.py news "what is the news?"
    python send_message.py events "any ongoing events?"
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.events_agent import BASE_URL as EVENTS_AGENT_BASE_URL
from agents.news_agent import BASE_URL as NEWS_AGENT_BASE_URL
from client import send_text_message

AGENT_URLS = {
    "news": NEWS_AGENT_BASE_URL,
    "events": EVENTS_AGENT_BASE_URL,
}


async def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in AGENT_URLS:
        print(f"Usage: python send_message.py <{'|'.join(AGENT_URLS)}> [message text]")
        raise SystemExit(1)

    agent = sys.argv[1]
    text = " ".join(sys.argv[2:]) or "what is the news?"

    reply = await send_text_message(AGENT_URLS[agent], text)
    print(reply)


if __name__ == "__main__":
    asyncio.run(main())
