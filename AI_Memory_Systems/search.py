"""Query helpers over the Cognee knowledge graph - one per search pattern
demonstrated in the tutorial: plain search, graph-completion, node-set
filtered, temporal, and feedback."""

import cognee
from cognee.modules.engine.models.node_set import NodeSet


async def basic_search(query_text: str):
    return await cognee.search(query_text)


async def graph_completion_search(query_text: str, save_interaction: bool = False):
    return await cognee.search(
        query_text=query_text,
        query_type=cognee.SearchType.GRAPH_COMPLETION,
        save_interaction=save_interaction,
    )


async def node_set_search(query_text: str, node_names: list[str]):
    """Graph-completion search scoped to one or more node sets (e.g. only
    'principles_data'), so answers draw from a specific domain of the graph."""
    return await cognee.search(
        query_text=query_text,
        query_type=cognee.SearchType.GRAPH_COMPLETION,
        node_type=NodeSet,
        node_name=node_names,
    )


async def temporal_search(query_text: str):
    return await cognee.search(query_text=query_text, query_type=cognee.SearchType.TEMPORAL)


async def submit_feedback(feedback_text: str, last_k: int = 1):
    """Record feedback on the last_k most recent search interactions saved
    with save_interaction=True, so the graph learns which results were useful."""
    return await cognee.search(
        query_type=cognee.SearchType.FEEDBACK,
        query_text=feedback_text,
        last_k=last_k,
    )
