"""Generates and opens an interactive HTML visualization of the knowledge graph."""

import webbrowser
from pathlib import Path

from cognee import visualize_graph

import config


async def generate_graph_visualization(output_path: Path = config.GRAPH_VISUALIZATION_PATH) -> Path:
    await visualize_graph(str(output_path))
    return output_path


def open_in_browser(html_path: Path) -> None:
    webbrowser.open(html_path.resolve().as_uri())
