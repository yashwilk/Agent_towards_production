"""Request/response schemas for the agent API."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class QueryRequest(BaseModel):
    query: str
    context: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "What is FastAPI?",
                "context": "I'm a beginner programmer.",
            }
        }
    )


class QueryResponse(BaseModel):
    response: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response": "FastAPI is a modern, high-performance web framework for building APIs with Python."
            }
        }
    )
