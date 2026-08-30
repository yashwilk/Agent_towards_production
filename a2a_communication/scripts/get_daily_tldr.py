"""CLI: fetch today's TLDR by querying the News and Events agents and combining their replies.

Requires both agent servers to be running (see run_news_agent.py / run_events_agent.py).
"""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from orchestrator import get_daily_tldr

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    print(asyncio.run(get_daily_tldr()))
