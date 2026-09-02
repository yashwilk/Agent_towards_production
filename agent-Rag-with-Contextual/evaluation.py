"""LM-Unit evaluation helpers."""

from typing import Dict, List

import pandas as pd
from tqdm import tqdm


def run_unit_tests_with_progress(client, df: pd.DataFrame, unit_tests: List[str]) -> List[Dict]:
    """
    Run unit tests with progress tracking and error handling.

    Args:
        client: ContextualAI client
        df: DataFrame with prompt-response pairs
        unit_tests: List of unit test strings

    Returns:
        List of test results
    """
    results = []

    for idx in tqdm(range(0, len(df)), desc="Processing responses"):
        row = df.iloc[idx]
        row_results = []

        for test in unit_tests:
            try:
                result = client.lmunit.create(
                    query=row["prompt"],
                    response=row["response"],
                    unit_test=test,
                )
                row_results.append(
                    {
                        "test": test,
                        "score": result.score,
                        "metadata": result.metadata if hasattr(result, "metadata") else None,
                    }
                )
            except Exception as e:
                print(f"Error with prompt {idx}, test '{test}': {e}")
                row_results.append({"test": test, "score": None, "error": str(e)})

        results.append(
            {
                "prompt": row["prompt"],
                "response": row["response"],
                "test_results": row_results,
            }
        )

    return results
