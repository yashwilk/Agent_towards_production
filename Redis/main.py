"""
Redis-backed travel agent demo: short-term memory (conversation state) persisted
via a Redis checkpointer, long-term memory (durable traveler facts) via a RedisVL
vector index - both embedded and reasoned over entirely by local Ollama models.
"""

from agent import build_agent
from long_term_memory import get_long_term_memory_index
from short_term_memory import get_checkpointer

THREAD_ID = "traveler-1"

DEMO_TURNS = [
    "Hi! I'm planning a trip to Japan and I love quiet, less touristy places.",
    "What kind of places would you suggest I visit, given what I just told you?",
]


def main() -> None:
    memory_index = get_long_term_memory_index()

    with get_checkpointer() as checkpointer:
        agent = build_agent(memory_index, checkpointer)
        run_config = {"configurable": {"thread_id": THREAD_ID}}

        for turn in DEMO_TURNS:
            result = agent.invoke({"messages": [("user", turn)]}, config=run_config)
            answer = result["messages"][-1].content
            print(f"\nYou: {turn}")
            print(f"Agent: {answer}")


if __name__ == "__main__":
    main()
