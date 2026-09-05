"""hushvert REST API client: format discovery and the submit/upload/poll/download
conversion flow (server lane only - the local lane runs as WebAssembly in the
browser and has no Python equivalent; see local-lane/example.ts)."""

import pathlib
import time
from typing import Optional

import requests

import config


def list_formats() -> list[dict]:
    """Return every server-side conversion pair hushvert supports, with its size cap and credit cost."""
    response = requests.get(f"{config.HUSHVERT_API}/v1/formats", timeout=30)
    response.raise_for_status()
    return response.json()["pairs"]


def check_usage() -> dict:
    """Return the remaining free-conversion allowance and credit balance."""
    headers = {"Authorization": f"Bearer {_require_api_key()}"}
    response = requests.get(f"{config.HUSHVERT_API}/v1/usage", headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def convert_file(path: str, to: str, idempotency_key: Optional[str] = None) -> bytes:
    """Convert a local file via the hushvert API: submit, upload, poll, download."""
    api_key = _require_api_key()

    src = pathlib.Path(path)
    data = src.read_bytes()
    pair = f"{src.suffix.lstrip('.').lower()}-to-{to}"

    headers = {"Authorization": f"Bearer {api_key}"}
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key

    submit = requests.post(
        f"{config.HUSHVERT_API}/v1/conversions",
        json={"pair": pair, "bytes": len(data)},
        headers=headers,
        timeout=30,
    )
    submit.raise_for_status()
    job = submit.json()

    requests.put(job["uploadUrl"], data=data, timeout=300).raise_for_status()

    while True:
        poll = requests.get(
            f"{config.HUSHVERT_API}/v1/conversions/{job['jobId']}",
            headers=headers,
            timeout=30,
        )
        poll.raise_for_status()
        state = poll.json()
        if state["status"] == "done":
            result = requests.get(state["downloadUrl"], timeout=300)
            result.raise_for_status()
            return result.content
        if state["status"] == "failed":
            raise RuntimeError(f"Conversion failed: {state.get('error')}")
        time.sleep(2)


def _require_api_key() -> str:
    if not config.HUSHVERT_API_KEY:
        raise RuntimeError(
            "Set the HUSHVERT_API_KEY environment variable before running this script "
            "(see .env.template)."
        )
    return config.HUSHVERT_API_KEY
