"""Shared building blocks for A2A agent servers.

Both agents in this project (news, events) are stateless: they take an
optional query string and return a single text answer. SimpleTextAgentExecutor
implements the A2A AgentExecutor contract once for that shape so individual
agent modules only need to provide a name and an async handler function.
"""

from __future__ import annotations

import logging
from typing import Awaitable, Callable, Optional

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard
from a2a.utils import new_agent_text_message
from starlette.applications import Starlette

logger = logging.getLogger(__name__)

QueryHandler = Callable[[Optional[str]], Awaitable[str]]


class SimpleTextAgentExecutor(AgentExecutor):
    """AgentExecutor for agents that answer with a single text message."""

    def __init__(self, agent_name: str, handler: QueryHandler):
        super().__init__()
        self._agent_name = agent_name
        self._handler = handler

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input() or None
        logger.info("%s executing task %s (query=%r)", self._agent_name, context.task_id, query)
        try:
            result = await self._handler(query)
            await event_queue.enqueue_event(new_agent_text_message(result))
        except Exception:
            logger.exception("%s failed to handle task %s", self._agent_name, context.task_id)
            await event_queue.enqueue_event(
                new_agent_text_message("Sorry, an error occurred while processing this request.")
            )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        logger.warning(
            "%s received a cancel request for task %s, but cancellation is not supported",
            self._agent_name,
            context.task_id,
        )
        await event_queue.enqueue_event(new_agent_text_message("Cancel is not supported by this agent."))


def build_app(agent_card: AgentCard, executor: AgentExecutor) -> Starlette:
    """Wires an executor into a request handler and builds the ASGI app for it."""
    request_handler = DefaultRequestHandler(agent_executor=executor, task_store=InMemoryTaskStore())
    return A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler).build()
