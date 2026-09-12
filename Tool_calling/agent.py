"""Builds the production multi-service agent: a LangGraph ReAct agent with
Gmail/Slack/Notion tools (via Arcade), each sensitive tool protected behind
human-in-the-loop approval."""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt.chat_agent_executor import create_react_agent

import config
from hitl import protect_tools
from tools import build_authorized_tools, build_tool_manager


def build_agent():
    checkpointer = MemorySaver()
    arcade_client, manager = build_tool_manager()
    tools = build_authorized_tools(arcade_client, manager)
    protected_tools = protect_tools(tools)

    return create_react_agent(
        model=config.CHAT_MODEL,
        prompt=config.SYSTEM_PROMPT,
        tools=protected_tools,
        checkpointer=checkpointer,
    )
