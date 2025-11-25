"""HTTP helper with retry/backoff for NLB API."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import httpx
from tenacity import AsyncRetrying, RetryError, retry_if_exception_type, stop_after_attempt, wait_exponential

from nlb_mcp.config import settings
from nlb_mcp.logging import get_logger, redact_headers


class UpstreamError(RuntimeError):
    """Raised when the upstream NLB API returns an error."""


async def get_json(path: str, params: Optional[Dict[str, str]] = None) -> Any:
    url = settings.nlb_api_base.rstrip("/") + path
    timeout = settings.request_timeout_ms / 1000

    headers = {
        "X-Api-Key": settings.nlb_api_key,
        "X-App-Code": settings.nlb_app_code,
    }
    log = get_logger()

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            async for attempt in AsyncRetrying(
                reraise=True,
                retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException, UpstreamError)),
                stop=stop_after_attempt(3),
                wait=wait_exponential(multiplier=0.3, min=0.3, max=2.0),
            ):
                with attempt:
                    log.info(
                        "nlb request start",
                        extra={
                            "path": path,
                            "params_keys": sorted(list(params.keys())) if params else [],
                            "attempt": attempt.retry_state.attempt_number,
                        },
                    )
                    response = await client.get(url, params=params, headers=headers)
                    if response.status_code >= 500:
                        raise UpstreamError(f"Upstream {response.status_code}")
                    response.raise_for_status()
                    log.info(
                        "nlb request ok",
                        extra={
                            "path": path,
                            "status": response.status_code,
                            "attempt": attempt.retry_state.attempt_number,
                            "headers": redact_headers(dict(response.headers)),
                        },
                    )
                    return response.json()
        except RetryError as exc:  # type: ignore[assignment]
            # Surface the last exception for clarity.
            raise exc.last_attempt.result()  # type: ignore[misc]


async def health_check() -> Dict[str, Any]:
    # Minimal readiness check (no network) since FastMCP handles auth externally.
    return {
        "status": "ok",
        "baseUrl": str(settings.nlb_api_base),
        "timeoutMs": settings.request_timeout_ms,
    }
