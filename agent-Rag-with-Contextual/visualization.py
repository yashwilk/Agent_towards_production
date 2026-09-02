"""Image display and unit-test radar-plot helpers."""

import base64
import io
from typing import Dict, List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from config import TEST_CATEGORY_MAPPING


def display_base64_image(base64_string: str, title: str = "Document") -> Image.Image:
    img_data = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_data))

    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis("off")
    plt.title(title)
    plt.show()

    return img


def display_retrieved_documents(client, agent_id: str, query_result) -> None:
    """Fetch and display the page image for every document referenced in a query result."""
    for i, retrieval_content in enumerate(query_result.retrieval_contents):
        print(f"\n--- Processing Document {i + 1} ---")

        ret_result = client.agents.query.retrieval_info(
            message_id=query_result.message_id,
            agent_id=agent_id,
            content_ids=[retrieval_content.content_id],
        )

        print(f"Retrieval Info for Document {i + 1}:")

        if ret_result.content_metadatas and ret_result.content_metadatas[0].page_img:
            base64_string = ret_result.content_metadatas[0].page_img
            display_base64_image(base64_string, f"Document {i + 1}")
        else:
            print(f"No image available for Document {i + 1}")

    print(f"\nTotal documents processed: {len(query_result.retrieval_contents)}")


def map_test_to_category(test_question: str) -> Optional[str]:
    """Map a full unit-test question to its short plot category."""
    for key, value in TEST_CATEGORY_MAPPING.items():
        if key in test_question.lower():
            return value
    return None


def create_unit_test_plots(
    results: List[Dict],
    test_indices: Optional[Union[int, List[int]]] = None,
    figsize: tuple = (10, 10),
):
    """
    Create polar plot(s) for unit test results. Can plot either a single test,
    specific multiple tests, or all tests in a row.

    Args:
        results: List of dictionaries containing test results
        test_indices: Optional; Either:
            - None (plots all results)
            - int (plots single result)
            - List[int] (plots multiple specific results)
        figsize: Tuple specifying the figure size (width, height)
    """
    if test_indices is None:
        indices_to_plot = list(range(len(results)))
    elif isinstance(test_indices, int):
        if test_indices >= len(results):
            raise IndexError(f"test_index {test_indices} is out of range. Only {len(results)} results available.")
        indices_to_plot = [test_indices]
    else:
        if not test_indices:
            raise ValueError("test_indices list cannot be empty")
        if max(test_indices) >= len(results):
            raise IndexError(f"test_index {max(test_indices)} is out of range. Only {len(results)} results available.")
        indices_to_plot = test_indices

    categories = ["ACCURACY", "CAUSATION", "SYNTHESIS", "LIMITATIONS", "EVIDENCE", "RELEVANCE"]

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    num_plots = len(indices_to_plot)
    fig_width = figsize[0] * num_plots
    fig = plt.figure(figsize=(fig_width, figsize[1]))

    for plot_idx, result_idx in enumerate(indices_to_plot):
        result = results[result_idx]

        ax = plt.subplot(1, num_plots, plot_idx + 1, projection="polar")

        scores = []
        for category in categories:
            score = None
            for test_result in result["test_results"]:
                if map_test_to_category(test_result["test"]) == category:
                    score = test_result["score"]
                    break
            scores.append(score if score is not None else 0)

        scores = np.concatenate((scores, [scores[0]]))

        ax.plot(angles, scores, "o-", linewidth=2)
        ax.fill(angles, scores, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 5)
        ax.grid(True)

        for angle, score, category in zip(angles[:-1], scores[:-1], categories):
            ax.text(angle, score + 0.2, f"{score:.2f}", ha="center", va="bottom")

        prompt = result["prompt"]
        ax.set_title(f"Test {result_idx}\n{prompt}", pad=20)

    plt.tight_layout()
    return fig
