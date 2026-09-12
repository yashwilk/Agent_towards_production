"""Human-in-the-loop protection: wraps sensitive tools so their execution
pauses for explicit user approval before running."""

import pprint
from typing import Callable

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, tool
from langgraph.types import interrupt

import config


def add_human_in_the_loop(target_tool: Callable | BaseTool) -> BaseTool:
    """Wrap a tool so its execution requires explicit human approval."""
    if not isinstance(target_tool, BaseTool):
        target_tool = tool(target_tool)

    @tool(target_tool.name, description=target_tool.description, args_schema=target_tool.args_schema)
    def call_tool_with_interrupt(config: RunnableConfig, **tool_input):
        arguments = pprint.pformat(tool_input, indent=4)
        response = interrupt(
            f"Do you allow the call to {target_tool.name} with arguments:\n{arguments}"
        )

        if response == "yes":
            return target_tool.invoke(tool_input, config)
        if response == "no":
            return "The User did not allow the tool to run"
        raise ValueError(f"Unsupported interrupt response type: {response}")

    return call_tool_with_interrupt


def protect_tools(tools: list) -> list:
    """Wrap only the tools named in config.PROTECTED_TOOL_NAMES, leaving
    read-only tools unchanged."""
    return [
        add_human_in_the_loop(t) if t.name in config.PROTECTED_TOOL_NAMES else t
        for t in tools
    ]


def yes_no_loop(prompt: str) -> str:
    """Force the user to answer yes or no to an approval prompt."""
    print(prompt)
    user_input = input("Your response [y/n]: ")
    while user_input.lower() not in ("y", "n"):
        user_input = input("Your response (must be 'y' or 'n'): ")
    return "yes" if user_input.lower() == "y" else "no"
