"""API key authentication dependency for the agent endpoints."""

from fastapi import Header, HTTPException

import config


async def verify_api_key(x_api_key: str = Header(None)) -> bool:
    """Verify the API key provided in the X-API-Key header.

    If no API_KEY is configured, validation is skipped - useful for local
    development. Once API_KEY is set, it's enforced on every request.
    """
    if not config.API_KEY:
        return True

    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key is missing")

    if x_api_key != config.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return True
