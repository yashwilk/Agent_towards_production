"""Creates Mem0 Memory instances from config."""

from typing import Optional

from mem0 import Memory

import config


def get_vector_memory() -> Memory:
    """Vector-only memory backed by Qdrant Cloud (Phase 1, always required)."""
    config.require_vector_store_config()
    memory = Memory.from_config(config.build_vector_config())
    print("Vector memory initialized (Qdrant).")
    return memory


def get_hybrid_memory() -> Optional[Memory]:
    """Vector + graph memory backed by Qdrant and Neo4j (Phase 2, optional).

    Returns None when Neo4j credentials aren't configured, so callers can fall
    back to vector-only memory instead of being forced through a setup prompt.
    """
    if not config.has_graph_store_config():
        print("Neo4j credentials not set; skipping hybrid (graph) memory.")
        return None

    config.require_vector_store_config()
    memory = Memory.from_config(config.build_hybrid_config())
    print("Hybrid memory initialized (Qdrant + Neo4j).")
    return memory
