"""FastAPI service exposing the agent over HTTP: a health check, a
synchronous query endpoint, and a token-streaming endpoint (SSE) - both
gated behind an optional API key (see auth.py).

Run with:
    python run_server.py
or directly:
    uvicorn main:app --reload
"""

import json

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

from agent import SimpleAgent
from auth import verify_api_key
from models import QueryRequest, QueryResponse

app = FastAPI(
    title="Agent API",
    description="A simple API that serves an AI agent",
    version="0.1.0",
)

agent = SimpleAgent()


@app.get("/health")
def health_check():
    """Check if the API is running."""
    return {"status": "ok", "message": "API is operational"}


@app.post("/agent", response_model=QueryResponse)
def query_agent(request: QueryRequest, authorized: bool = Depends(verify_api_key)):
    """Get a response from the agent."""
    response = agent.generate_response(request.query)
    return QueryResponse(response=response)


@app.post("/agent/stream")
async def stream_agent(request: QueryRequest, authorized: bool = Depends(verify_api_key)):
    """Stream a response from the agent token by token over SSE."""

    async def event_generator():
        async for token in agent.generate_response_stream(request.query):
            data = json.dumps({"token": token})
            yield f"data: {data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
