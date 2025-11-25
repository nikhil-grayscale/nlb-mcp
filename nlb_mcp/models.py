"""Lightweight response and normalized types."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class TitleSummary(TypedDict, total=False):
    title: str
    author: str
    isbn: str
    bibId: str
    publisher: str
    publishYear: str
    formats: List[str]
    subjects: List[str]


class NormalizedAvailability(TypedDict, total=False):
    branch: str
    callNumber: str
    status: str
    available: int
    total: int


def normalize_titles(response: Dict[str, Any]) -> List[TitleSummary]:
    titles = response.get("Result", {}).get("Titles", []) if isinstance(response, dict) else []
    normalized: List[TitleSummary] = []
    for item in titles:
        normalized.append(
            {
                "title": item.get("TitleName"),
                "author": item.get("AuthorName"),
                "isbn": item.get("ISBN"),
                "bibId": item.get("BID"),
                "publisher": item.get("Publisher"),
                "publishYear": item.get("PublishYear"),
                "formats": [item["Category"]] if item.get("Category") else [],
                "subjects": item.get("Subjects") or [],
            }
        )
    return normalized


def normalize_availability(response: Dict[str, Any]) -> List[NormalizedAvailability]:
    items = response.get("Result", {}).get("Items", []) if isinstance(response, dict) else []
    normalized: List[NormalizedAvailability] = []
    for item in items:
        normalized.append(
            {
                "branch": item.get("BranchName") or item.get("BranchID") or "Unknown branch",
                "callNumber": item.get("CallNumber"),
                "status": item.get("Status"),
                "available": item.get("Available"),
                "total": item.get("Total"),
            }
        )
    return normalized
