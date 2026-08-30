"""Standalone entrypoint for the News Information Agent server."""

import logging
import os
import sys
from pathlib import Path

import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.news_agent import BASE_URL, create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting News Agent server on {BASE_URL}")
    uvicorn.run(
        create_app(),
        host=os.getenv("NEWS_AGENT_HOST", "0.0.0.0"),
        port=int(os.getenv("NEWS_AGENT_PORT", "9001")),
    )
