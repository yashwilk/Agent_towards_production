"""Configuration for the FastAPI agent service.

Loads .env for the optional API key and server host/port. When API_KEY is
unset, auth.verify_api_key skips validation - useful for local development,
enforced once a real key is configured (e.g. in production).
"""

import os

from dotenv import load_dotenv

load_dotenv()

AGENT_NAME = os.environ.get("AGENT_NAME", "FastAPI Agent")
API_KEY = os.getenv("API_KEY")

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
