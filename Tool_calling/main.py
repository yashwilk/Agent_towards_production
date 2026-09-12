"""Interactive CLI for the production Arcade tool-calling agent: a LangGraph
ReAct agent with Gmail, Slack, and Notion access, protected by human-in-the-
loop approval on any tool that sends or writes data.

The first run walks you through Arcade's OAuth flow for each provider - open
the printed URL and approve access. Authorization then persists for your
ARCADE_USER_ID on future runs.

Run with:
    python main.py
"""

from agent import build_agent
from chat import interactive_chat, new_thread_config
import config


def main() -> None:
    agent = build_agent()
    thread_config = new_thread_config(user_id=config.ARCADE_USER_ID)
    print(f"thread_id = {thread_config['configurable']['thread_id']}")
    print("Ask me to check your email, post to Slack, or manage a Notion page. Type 'exit' to quit.")
    interactive_chat(agent, thread_config)


if __name__ == "__main__":
    main()
