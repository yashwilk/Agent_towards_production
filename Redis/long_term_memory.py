"""Long-term memory: a RedisVL vector index over semantic/episodic memories,
embedded locally via Ollama (nomic-embed-text)."""

from typing import List, Optional

from langchain_ollama import OllamaEmbeddings
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.query.filter import Tag
from redisvl.schema.schema import IndexSchema

import config
from models import MemoryType, StoredMemory

_embedder = OllamaEmbeddings(model=config.OLLAMA_EMBEDDING_MODEL, base_url=config.OLLAMA_BASE_URL)

MEMORY_SCHEMA = IndexSchema.from_dict(
    {
        "index": {
            "name": config.LONG_TERM_MEMORY_INDEX,
            "prefix": "memory",
            "key_separator": ":",
            "storage_type": "json",
        },
        "fields": [
            {"name": "content", "type": "text"},
            {"name": "memory_type", "type": "tag"},
            {"name": "metadata", "type": "text"},
            {"name": "created_at", "type": "text"},
            {"name": "user_id", "type": "tag"},
            {"name": "memory_id", "type": "tag"},
            {
                "name": "embedding",
                "type": "vector",
                "attrs": {
                    "algorithm": "flat",
                    "dims": config.EMBEDDING_DIMS,
                    "distance_metric": "cosine",
                    "datatype": "float32",
                },
            },
        ],
    }
)


def get_long_term_memory_index() -> SearchIndex:
    index = SearchIndex(MEMORY_SCHEMA, redis_url=config.REDIS_URL)
    index.create(overwrite=False)  # no-op if the index already exists
    return index


def add_memory(
    index: SearchIndex,
    content: str,
    memory_type: MemoryType,
    user_id: Optional[str] = None,
    metadata: str = "",
) -> StoredMemory:
    """Embed and store a single long-term memory."""
    stored = StoredMemory(
        content=content,
        memory_type=memory_type,
        metadata=metadata,
        user_id=user_id,
    )

    embedding = _embedder.embed_query(content)

    keys = index.load(
        [
            {
                "content": stored.content,
                "memory_type": stored.memory_type.value,
                "metadata": stored.metadata,
                "created_at": stored.created_at.isoformat(),
                "user_id": stored.user_id or "",
                "memory_id": stored.memory_id,
                "embedding": embedding,
            }
        ],
        id_field="memory_id",
    )
    stored.id = keys[0]
    return stored


def search_memories(
    index: SearchIndex, query: str, user_id: Optional[str] = None, top_k: int = 5
) -> List[dict]:
    """Semantic search over stored long-term memories."""
    embedding = _embedder.embed_query(query)

    vector_query = VectorQuery(
        vector=embedding,
        vector_field_name="embedding",
        return_fields=["content", "memory_type", "metadata", "created_at", "user_id"],
        num_results=top_k,
        filter_expression=(Tag("user_id") == user_id) if user_id else None,
    )

    return index.query(vector_query)
