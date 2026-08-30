"""Standalone entrypoint for the Current Events Information Agent server."""

import logging
import os
import sys
from pathlib import Path

import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.events_agent import BASE_URL, create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting Events Agent server on {BASE_URL}")
    uvicorn.run(
        create_app(),
        host=os.getenv("EVENTS_AGENT_HOST", "0.0.0.0"),
        port=int(os.getenv("EVENTS_AGENT_PORT", "9002")),
    )
