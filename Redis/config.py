"""Configuration for the Redis-backed travel agent (short-term + long-term memory).

Runs entirely on local models: Ollama for chat and for embeddings, so no API key
is required to run this project.
"""

import os

from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_EMBEDDING_MODEL = os.environ.get("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_DIMS = 768  # nomic-embed-text's output size

LONG_TERM_MEMORY_INDEX = "agent_memories"
