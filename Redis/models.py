"""Pydantic models for the agent's long-term memory."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

import ulid
from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class Memory(BaseModel):
    """A single long-term memory."""

    content: str
    memory_type: MemoryType
    metadata: str = ""


class Memories(BaseModel):
    """A list of memories extracted from a conversation by an LLM.

    NOTE: structured-output tooling generally requires a list to be wrapped in
    an object like this rather than returned bare.
    """

    memories: List[Memory]


class StoredMemory(Memory):
    """A memory as stored in Redis, with its generated identifiers."""

    id: str = ""  # the Redis key, filled in once redisvl generates it
    memory_id: str = Field(default_factory=lambda: str(ulid.ULID()))
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    thread_id: Optional[str] = None
