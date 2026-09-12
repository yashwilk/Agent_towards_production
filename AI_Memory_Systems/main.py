"""Demo: build a Cognee knowledge graph from Guido van Rossum's Python
contributions, PEP/Zen philosophy docs, and personal dev notes, then run the
searches from the tutorial against it - graph completion, cross-domain,
node-set filtered, temporal, and feedback.

Writes an interactive guido_contributions.html graph visualization. Run with:
    python main.py
"""

import asyncio

import config
from ingest import build_graph, build_memory_layer
from search import (
    basic_search,
    graph_completion_search,
    node_set_search,
    submit_feedback,
    temporal_search,
)
from visualize import generate_graph_visualization, open_in_browser


async def main() -> None:
    await build_graph()

    initial = await basic_search("Show me commits")
    print("Initial search result:", initial[0] if initial else "No results")

    html_path = await generate_graph_visualization()
    print(f"Graph visualization written to {html_path}")
    open_in_browser(html_path)

    cross_domain = await graph_completion_search(
        "What validation issues did I encounter in January 2024, and how "
        "would they be addressed in Guido's contributions?"
    )
    print("Cross-domain analysis:", cross_domain)

    # memify() infers implicit rules/relationships across the graph, built on
    # top of everything ingested so far.
    await build_memory_layer()

    pattern_analysis = await graph_completion_search(
        "How does my AsyncWebScraper implementation align with Python's design principles?"
    )
    print("Python pattern analysis:", pattern_analysis)

    naming_guidance = await node_set_search(
        "How should variables be named?", node_names=[config.PRINCIPLES_NODE_SET]
    )
    print("Naming guidance (principles_data only):", naming_guidance)

    temporal_insight = await temporal_search("What can we learn from Guido's contributions in 2025?")
    print("Temporal insight:", temporal_insight)

    zen_answer = await graph_completion_search(
        "What is the most zen thing about Python?", save_interaction=True
    )
    print("Zen answer:", zen_answer)

    feedback = await submit_feedback(
        "Last result was useful, I like code that complies with best practices.", last_k=1
    )
    print("Feedback recorded:", feedback)


if __name__ == "__main__":
    asyncio.run(main())
