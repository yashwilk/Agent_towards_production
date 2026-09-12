"""Utilities for running a compiled LangGraph agent from the terminal,
including resolving human-in-the-loop approval interrupts."""

import uuid

from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from hitl import yes_no_loop


def run_graph(graph: CompiledStateGraph, config, input) -> None:
    for event in graph.stream(input, config=config, stream_mode="values"):
        if "messages" in event:
            event["messages"][-1].pretty_print()


def handle_interrupts(graph: CompiledStateGraph, config) -> None:
    """Resolve any pending human-in-the-loop approval requests on the graph's
    current state, resuming execution with the user's decision."""
    for interr in graph.get_state(config).interrupts:
        approved = yes_no_loop(interr.value)
        run_graph(graph, config, Command(resume=approved))


def new_thread_config(user_id: str | None = None) -> dict:
    """A fresh LangGraph config for a new conversation thread. Arcade tools
    need user_id on the config to know which user's authorization to use."""
    configurable = {"thread_id": uuid.uuid4()}
    if user_id:
        configurable["user_id"] = user_id
    return {"configurable": configurable}


def interactive_chat(graph: CompiledStateGraph, thread_config: dict) -> None:
    """Run an interactive terminal chat loop against the agent, resolving any
    human-in-the-loop approval prompts as they occur. Type 'exit' to quit."""
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        user_message = {"messages": [HumanMessage(content=user_input)]}
        run_graph(graph, thread_config, user_message)
        handle_interrupts(graph, thread_config)
