"""Thin client wrapping NLB endpoints."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .http_client import get_json


async def search_titles(
    *, keywords: str, source: Optional[str] = None, limit: Optional[int] = None, sort_fields: Optional[str] = None
) -> Dict[str, Any]:
    params: Dict[str, str] = {"Keywords": keywords}
    if source:
        params["Source"] = source
    if limit:
        params["Limit"] = str(limit)
    if sort_fields:
        params["SortFields"] = sort_fields

    return await get_json("/SearchTitles", params)


async def get_titles(
    *,
    keywords: Optional[str] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    subject: Optional[str] = None,
    isbn: Optional[str] = None,
    limit: Optional[int] = None,
    sort_fields: Optional[str] = None,
    set_id: Optional[int] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
    params: Dict[str, str] = {}
    if keywords:
        params["Keywords"] = keywords
    if title:
        params["Title"] = title
    if author:
        params["Author"] = author
    if subject:
        params["Subject"] = subject
    if isbn:
        params["ISBN"] = isbn
    if limit:
        params["Limit"] = str(limit)
    if sort_fields:
        params["SortFields"] = sort_fields
    if set_id is not None:
        params["SetId"] = str(set_id)
    if offset is not None:
        params["Offset"] = str(offset)

    return await get_json("/GetTitles", params)


async def get_availability(
    *, bib_id: Optional[str] = None, isbn: Optional[str] = None, control_no: Optional[str] = None, branch_id: Optional[str] = None
) -> Dict[str, Any]:
    params: Dict[str, str] = {}
    if bib_id:
        params["BID"] = bib_id
    if isbn:
        params["ISBN"] = isbn
    if control_no:
        params["ControlNo"] = control_no
    if branch_id:
        params["BranchID"] = branch_id

    return await get_json("/GetAvailabilityInfo", params)
