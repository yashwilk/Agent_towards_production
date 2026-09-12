"""Builds the Cognee knowledge graph from the tutorial's data sources.

Two ingestion stages, matching the tutorial: Guido van Rossum's mypy/CPython
contributions are added and cognified first (establishing the temporal graph
foundation), then the remaining developer-context and Python-philosophy
sources are added and cognified into the same graph.

Run standalone with `python ingest.py`, or call build_graph() from main.py.
"""

import asyncio

import cognee

import config


async def reset_graph() -> None:
    """Wipe any existing Cognee data/graph so ingestion starts from a clean state."""
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)


async def ingest_guido_contributions() -> None:
    """Ingest Guido van Rossum's mypy/CPython contributions with temporal awareness."""
    await cognee.add(str(config.GUIDO_CONTRIBUTIONS_FILE), node_set=[config.GUIDO_NODE_SET])
    await cognee.cognify(temporal_cognify=True)


async def ingest_remaining_sources() -> None:
    """Ingest personal developer context plus PEP/Zen philosophy references."""
    await cognee.add(str(config.COPILOT_CONVERSATIONS_FILE), node_set=[config.DEVELOPER_NODE_SET])
    await cognee.add(str(config.DEVELOPER_RULES_FILE), node_set=[config.DEVELOPER_NODE_SET])
    await cognee.add(str(config.ZEN_PRINCIPLES_FILE), node_set=[config.PRINCIPLES_NODE_SET])
    await cognee.add(str(config.PEP_STYLE_GUIDE_FILE), node_set=[config.PRINCIPLES_NODE_SET])
    await cognee.cognify(temporal_cognify=True)


async def build_memory_layer() -> None:
    """Infer implicit rules and cross-source relationships (the memify step)."""
    await cognee.memify()


async def build_graph() -> None:
    await reset_graph()
    await ingest_guido_contributions()
    await ingest_remaining_sources()


if __name__ == "__main__":
    asyncio.run(build_graph())
