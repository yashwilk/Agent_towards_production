"""Demo: ask the hybrid research agent questions that require both live web
search and internal CRM vector search, and stream its reasoning.

Populate the vector store first with `python ingest.py` if you want the
Internal Vector Search tool to have real CRM documents to draw on.
"""

from langchain_core.messages import HumanMessage

from agent import build_agent

DEMO_QUESTIONS = [
    "Search for the latest news on Google relevant to our current CRM data on them.",
    "Check Google's deal size and find their latest earnings report to validate if they are on a spending spree.",
]


def run_demo(agent) -> None:
    for question in DEMO_QUESTIONS:
        print(f"\nYou: {question}")
        inputs = {"messages": [HumanMessage(content=question)]}
        for step in agent.stream(inputs, stream_mode="values"):
            message = step["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()


def main() -> None:
    agent = build_agent()
    run_demo(agent)


if __name__ == "__main__":
    main()
