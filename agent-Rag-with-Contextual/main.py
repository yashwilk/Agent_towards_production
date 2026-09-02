"""
Contextual AI RAG demo: ingest financial PDFs into a datastore, query a
grounded agent, inspect retrieved source pages, and score responses with
LM-Unit tests.
"""

import pandas as pd
from contextual import ContextualAI

import config
from agent_utils import get_or_create_agent, populate_eval_responses, query_agent
from datastore_utils import (
    download_and_ingest_documents,
    get_or_create_datastore,
    print_first_document_metadata,
)
from evaluation import run_unit_tests_with_progress
from visualization import create_unit_test_plots, display_retrieved_documents


def main():
    client = ContextualAI(api_key=config.API_KEY)

    # 1. Datastore: isolated, secure storage per use case, with automatic
    #    parsing/chunking/indexing and optimized retrieval.
    datastore_id = get_or_create_datastore(client, config.DATASTORE_NAME)

    document_ids = download_and_ingest_documents(
        client, datastore_id, config.FILES_TO_UPLOAD, config.DATA_DIR
    )
    print_first_document_metadata(client, datastore_id, document_ids)

    # 2. Agent: grounded assistant scoped to the datastore.
    agent_id = get_or_create_agent(
        client,
        agent_name=config.AGENT_NAME,
        datastore_id=datastore_id,
        system_prompt=config.SYSTEM_PROMPT,
        suggested_queries=config.SUGGESTED_QUERIES,
    )

    query_result = query_agent(client, agent_id, config.DEMO_QUERY)
    print(query_result.message.content)

    # 3. Show the source document pages the agent grounded its answer on.
    display_retrieved_documents(client, agent_id, query_result)

    # 4. LM-Unit: score a single response against one unit test.
    sample_response = """NVIDIA's Data Center revenue for Q4 FY25 was $35,580 million.\\[1\\]()

This represents a significant increase from the previous quarter (Q3 FY25) when Data Center revenue was $30,771 million.[1]()

The full quarterly trend for Data Center revenue in FY25 was:
- Q4 FY25: $35,580 million
- Q3 FY25: $30,771 million
- Q2 FY25: $26,272 million
- Q1 FY25: $22,563 million[1]()
"""
    unit_result = client.lmunit.create(
        query="What was NVIDIA's Data Center revenue in Q4 FY25?",
        response=sample_response,
        unit_test="Does the response avoid unnecessary information?",
    )
    print(unit_result)

    # 5. Build an eval set, query the agent for each prompt, and save it.
    eval_df = pd.DataFrame({"prompt": config.EVAL_QUERIES})
    eval_df["response"] = ""
    eval_df = populate_eval_responses(client, agent_id, eval_df)

    print(eval_df[["prompt", "response"]])
    eval_df.to_csv("eval_input.csv", index=False)

    # 6. Score every eval response against every unit test.
    results = run_unit_tests_with_progress(client, eval_df, config.UNIT_TESTS)

    pd.DataFrame(
        [
            (r["prompt"], r["response"], t["test"], t["score"])
            for r in results
            for t in r["test_results"]
        ],
        columns=["prompt", "response", "test", "score"],
    ).to_csv("unit_test_results.csv", index=False)

    for result in results[:2]:
        print(f"\nPrompt: {result['prompt']}")
        print(f"Response: {result['response']}")
        print("Test Results:")
        for test_result in result["test_results"]:
            print(f"- {test_result['test']}: {test_result['score']}")

    # 7. Visualize the per-category scores as radar plots.
    create_unit_test_plots(results, test_indices=[0, 1, 2])
    create_unit_test_plots(results, test_indices=[3, 4, 5])


if __name__ == "__main__":
    main()
