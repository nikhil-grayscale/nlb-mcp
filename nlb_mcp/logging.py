"""Lightweight logging setup with basic redaction."""

from __future__ import annotations

import logging
from typing import Any, Dict


_logger = logging.getLogger("nlb_mcp")
if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
_logger.setLevel(logging.INFO)
_logger.propagate = False


def get_logger() -> logging.Logger:
    return _logger


def redact_headers(headers: Dict[str, Any]) -> Dict[str, Any]:
    # Remove or mask secret-bearing headers before logging.
    redacted = {}
    for key, value in headers.items():
        if key.lower() in {"x-api-key", "x-app-code"}:
            redacted[key] = "***"
        else:
            redacted[key] = value
    return redacted
