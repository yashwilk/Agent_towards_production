"""Configuration for the Mem0 personal research assistant.

Phase 1 (vector memory via Qdrant Cloud) is required. Phase 2 (graph memory via
Neo4j) is optional and only activates when its environment variables are set.
"""

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMS = 3072

DEFAULT_USER_ID = "researcher"


def require_vector_store_config() -> None:
    missing = [
        name
        for name, value in [
            ("OPENAI_API_KEY", OPENAI_API_KEY),
            ("QDRANT_URL", QDRANT_URL),
            ("QDRANT_API_KEY", QDRANT_API_KEY),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(
            f"Missing required environment variable(s): {', '.join(missing)}. See .env.template."
        )


def has_graph_store_config() -> bool:
    return bool(NEO4J_URI and NEO4J_USERNAME and NEO4J_PASSWORD)


def build_vector_config(collection_name: str = "research_assistant_vectors") -> dict:
    return {
        "llm": {
            "provider": "openai",
            "config": {
                "model": LLM_MODEL,
                "temperature": 0.1,
                "max_tokens": 2000,
            },
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": EMBEDDING_MODEL,
                "embedding_dims": EMBEDDING_DIMS,
            },
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "url": QDRANT_URL,
                "api_key": QDRANT_API_KEY,
                "collection_name": collection_name,
                "embedding_model_dims": EMBEDDING_DIMS,
            },
        },
        "version": "v1.1",
    }


def build_hybrid_config(collection_name: str = "research_assistant_hybrid") -> dict:
    """Vector config plus a Neo4j graph store, for richer relationship-aware recall."""
    hybrid = build_vector_config(collection_name)
    hybrid["graph_store"] = {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URI,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD,
        },
    }
    return hybrid
