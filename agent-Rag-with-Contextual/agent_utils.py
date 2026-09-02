"""Agent creation and querying helpers."""

from typing import List

import pandas as pd


def get_or_create_agent(
    client,
    agent_name: str,
    datastore_id: str,
    system_prompt: str,
    suggested_queries: List[str],
) -> str:
    """Return the ID of an existing agent with this name, creating one if needed."""
    agents = client.agents.list()
    existing_agent = next((agent for agent in agents if agent.name == agent_name), None)

    if existing_agent:
        print(f"Using existing agent with ID: {existing_agent.id}")
        return existing_agent.id

    print("Creating new agent")
    app_response = client.agents.create(
        name=agent_name,
        description="Helpful Grounded AI Assistant",
        datastore_ids=[datastore_id],
        system_prompt=system_prompt,
        agent_configs={
            "global_config": {
                "enable_multi_turn": False,  # Turning this off for deterministic responses for this demo
            }
        },
        suggested_queries=suggested_queries,
    )

    agent_id = app_response.id
    print(f"Agent ID created: {agent_id}")
    return agent_id


def query_agent(client, agent_id: str, query: str):
    return client.agents.query.create(
        agent_id=agent_id,
        messages=[{"content": query, "role": "user"}],
    )


def populate_eval_responses(client, agent_id: str, eval_df: pd.DataFrame) -> pd.DataFrame:
    """Run each prompt in eval_df through the agent and fill in the 'response' column."""
    for index, row in eval_df.iterrows():
        try:
            query_result = query_agent(client, agent_id, row["prompt"])
            eval_df.at[index, "response"] = query_result.message.content
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            eval_df.at[index, "response"] = f"Error: {e}"

    return eval_df
