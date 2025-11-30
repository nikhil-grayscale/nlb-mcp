"""FastMCP server definition for the NLB Singapore MCP server (Python)."""

from __future__ import annotations

# Ensure package root is on sys.path when invoked as a file (e.g., fastmcp inspect /app/nlb_mcp/server.py).
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastmcp import FastMCP

from nlb_mcp.branches import BRANCHES
from nlb_mcp.config import settings
from nlb_mcp.http_client import health_check as basic_health
from nlb_mcp.logging import get_logger
from nlb_mcp.models import (
    NormalizedAvailability,
    SearchTitlesResponseV2,
    normalize_availability,
    normalize_titles,
)
from nlb_mcp.nlb_client import get_availability, get_titles, search_titles

def _clamp_limit(value: Optional[int]) -> Optional[int]:
    if value is None:
        return None
    if value < 1:
        raise ValueError("limit must be >= 1")
    return min(value, 100)


def _validate_sort(sort_fields: Optional[str]) -> Optional[str]:
    if sort_fields and len(sort_fields) > 100:
        raise ValueError("sort_fields too long; max 100 characters")
    return sort_fields


def _validate_identifiers(bib_id: Optional[str], isbn: Optional[str], control_no: Optional[str]) -> None:
    if not (bib_id or isbn or control_no):
        raise ValueError("Provide at least one identifier: bib_id, isbn, or control_no")


async def health_check() -> dict:
    # FastMCP handles OAuth2; this only verifies configuration is loaded.
    return await basic_health()


async def tool_search_titles(
    keywords: str,
    limit: Optional[int] = None,
    sort_fields: Optional[str] = None,
    source: Optional[str] = None,
) -> List[Dict[str, Any]]:
    log = get_logger()
    log.info(
        "tool search_titles called",
        extra={"has_keywords": bool(keywords and keywords.strip()), "has_source": bool(source)},
    )
    response = await search_titles(
        keywords=keywords.strip(),
        limit=_clamp_limit(limit),
        sort_fields=_validate_sort(sort_fields),
        source=source.strip() if source else None,
    )
    return _basic_titles(_limit_titles(normalize_titles(response), 5))


async def tool_get_titles(
    keywords: Optional[str] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    subject: Optional[str] = None,
    isbn: Optional[str] = None,
    limit: Optional[int] = None,
    sort_fields: Optional[str] = None,
    set_id: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    log = get_logger()
    log.info(
        "tool search_titles_advanced called",
        extra={
            "has_keywords": bool(keywords and keywords.strip()),
            "has_title": bool(title and title.strip()),
            "has_author": bool(author and author.strip()),
            "has_subject": bool(subject and subject.strip()),
            "has_isbn": bool(isbn and isbn.strip()),
        },
    )
    response = await get_titles(
        keywords=keywords.strip() if keywords else None,
        title=title.strip() if title else None,
        author=author.strip() if author else None,
        subject=subject.strip() if subject else None,
        isbn=isbn.strip() if isbn else None,
        limit=_clamp_limit(limit),
        sort_fields=_validate_sort(sort_fields),
        set_id=set_id,
        offset=offset,
    )
    return _basic_titles(_limit_titles(normalize_titles(response), 5))


async def tool_availability(
    bib_id: Optional[str] = None,
    isbn: Optional[str] = None,
    control_no: Optional[str] = None,
    branch_id: Optional[str] = None,
) -> list[NormalizedAvailability]:
    log = get_logger()
    _validate_identifiers(bib_id, isbn, control_no)
    log.info(
        "tool availability_by_title called",
        extra={
            "has_bib": bool(bib_id),
            "has_isbn": bool(isbn),
            "has_control": bool(control_no),
            "has_branch": bool(branch_id),
        },
    )

    response = await get_availability(
        bib_id=bib_id.strip() if bib_id else None,
        isbn=isbn.strip() if isbn else None,
        control_no=control_no.strip() if control_no else None,
        branch_id=branch_id.strip() if branch_id else None,
    )
    return normalize_availability(response)


async def tool_availability_at_branch(
    branch_id: str,
    bib_id: Optional[str] = None,
    isbn: Optional[str] = None,
    control_no: Optional[str] = None,
) -> list[NormalizedAvailability]:
    # Require a branch plus at least one identifier to avoid broad queries.
    if not branch_id:
        raise ValueError("branch_id is required")
    _validate_identifiers(bib_id, isbn, control_no)
    log = get_logger()
    log.info(
        "tool availability_at_branch called",
        extra={
            "has_bib": bool(bib_id),
            "has_isbn": bool(isbn),
            "has_control": bool(control_no),
            "branch": branch_id,
        },
    )

    response = await get_availability(
        bib_id=bib_id.strip() if bib_id else None,
        isbn=isbn.strip() if isbn else None,
        control_no=control_no.strip() if control_no else None,
        branch_id=branch_id.strip(),
    )
    return normalize_availability(response)


def _limit_titles(results: List[SearchTitlesResponseV2], max_titles: int) -> List[SearchTitlesResponseV2]:
    if not results:
        return results
    first = results[0]
    titles = first.get("titles") or []
    trimmed = titles[:max_titles]
    first["titles"] = trimmed
    if "count" in first and first["count"] is not None:
        first["count"] = min(first["count"], len(trimmed))
    return results


def _basic_titles(results: List[SearchTitlesResponseV2]) -> List[Dict[str, Any]]:
    if not results:
        return []
    data = results[0]
    titles = data.get("titles") or []
    basics: List[Dict[str, Any]] = []
    for title in titles:
        recs = []
        for rec in title.get("records", []):
            fmt = rec.get("format")
            if isinstance(fmt, dict):
                fmt = fmt.get("name") or fmt.get("code")
            recs.append(
                _strip_nones(
                    {
                        "brn": rec.get("brn"),
                        "format": fmt,
                        "availability": rec.get("availability"),
                    }
                )
            )
        basics.append(
            _strip_nones(
                {
                    "title": title.get("title"),
                    "records": recs,
                }
            )
        )
    return basics


def _strip_nones(obj: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in obj.items() if v is not None}

async def tool_list_branches(filter: Optional[str] = None) -> list[dict]:
    # Return branch code/name pairs; optional substring filter on code or name.
    if not filter:
        return BRANCHES
    term = filter.lower()
    return [b for b in BRANCHES if term in b["code"].lower() or term in b["name"].lower()]


def create_server() -> FastMCP:
    """
    Create and return the FastMCP server.

    Kept synchronous to avoid event loop issues during `fastmcp inspect`.
    """
    # Initialize settings early to fail fast on missing env vars.
    _ = settings

    server = FastMCP(
        name="nlb-mcp",
        version="0.1.0",
    )

    # Register tools. The decorator form is not used to keep explicit names/handlers clear.
    server.tool(name="health_check", description="Validate config and startup readiness.")(health_check)
    server.tool(
        name="search_titles",
        description="Search NLB catalogue by keyword (BRN/ISBN/Title/Author/Subject).",
    )(tool_search_titles)
    server.tool(
        name="search_titles_advanced",
        description="Fielded search for titles with optional author/subject/ISBN filters and pagination.",
    )(tool_get_titles)
    server.tool(
        name="availability_by_title",
        description="Get item availability for a title/ISBN with branch breakdown.",
    )(tool_availability)
    server.tool(
        name="availability_at_branch",
        description="Get item availability for a title/ISBN at a specific branch.",
    )(tool_availability_at_branch)
    server.tool(
        name="list_branches",
        description="List branch codes and names (C005 Library Location). Optional substring filter via 'filter'.",
    )(tool_list_branches)

    # Expose usage prompt as a resource if the FastMCP server supports resource registration.
    usage_path = Path(__file__).resolve().parent / "usage.md"
    register_resource = getattr(server, "resource", None) or getattr(server, "add_resource", None)
    if callable(register_resource):
        register_resource(
            {
                "name": "usage",
                "description": "Usage guide for NLB MCP tools",
                "path": str(usage_path),
            }
        )

    return server


# Eagerly create the server object for discovery without starting event loops.
server = mcp = app = create_server()

__all__ = ["create_server", "server", "mcp", "app"]
