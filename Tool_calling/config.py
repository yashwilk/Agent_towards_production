"""Configuration for the Arcade-powered multi-service tool-calling agent.

Loads .env for the OpenAI + Arcade credentials, and centralizes the chat
model and the Arcade tools/toolkits this agent is granted access to.
"""

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ARCADE_API_KEY = os.getenv("ARCADE_API_KEY")
# Must match the email address used to create the Arcade account, so tool
# authorizations and OAuth tokens are associated with the right user.
ARCADE_USER_ID = os.getenv("ARCADE_USER_ID")

CHAT_MODEL = os.environ.get("CHAT_MODEL", "openai:gpt-5")

# Registered via manager.init_tools() - returns usable tool objects directly.
INIT_TOOLS = ["Gmail_ListEmails"]
# Registered via manager.add_tool() - collected later through to_langchain().
ADDED_TOOLS = ["Gmail.SendEmail"]
# Whole toolkits registered via manager.add_toolkit().
TOOLKITS = ["Slack", "NotionToolkit"]

# Tools that send or write data externally - wrapped with human-in-the-loop
# approval so the agent can't act on them without explicit user consent.
PROTECTED_TOOL_NAMES = [
    "Gmail_SendEmail",
    "Slack_SendDmToUser",
    "Slack_SendMessage",
    "Slack_SendMessageToChannel",
    "NotionToolkit_AppendContentToEndOfPage",
    "NotionToolkit_CreatePage",
]

SYSTEM_PROMPT = (
    "You are a helpful assistant that can help with everyday tasks."
    " If the user's request is confusing you must ask them to clarify"
    " their intent, and fulfill the instruction to the best of your"
    " ability. Be concise and friendly at all times."
    " Use the Gmail tools to address requests about reading or sending emails."
    " Use the Slack tools to address requests about interactions with users and channels in Slack."
    " Use the Notion tools to address requests about managing content in Notion Pages."
    " In general, when possible, use the most relevant tool for the job."
)
