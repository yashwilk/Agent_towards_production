"""Short-term memory: conversation state persisted in Redis via LangGraph's
built-in checkpointer, so a conversation thread survives across process runs."""

from contextlib import contextmanager

from langgraph.checkpoint.redis import RedisSaver

import config


@contextmanager
def get_checkpointer():
    with RedisSaver.from_conn_string(config.REDIS_URL) as saver:
        saver.setup()
        yield saver
