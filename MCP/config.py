"""Configuration for the Ollama-powered MCP crypto agent."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = Path(__file__).resolve().parent
CRYPTO_SERVER_SCRIPT = str(PROJECT_DIR / "server" / "crypto_server.py")

# Spawn the MCP server with this same interpreter, so it runs inside whatever
# environment (e.g. this project's .venv) main.py itself is running in.
PYTHON_EXECUTABLE = sys.executable

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
