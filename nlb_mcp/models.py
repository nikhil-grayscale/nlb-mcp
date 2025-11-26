"""Lightweight response and normalized types."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class TitleSummary(TypedDict, total=False):
    title: str
    author: str
    isbn: str
    bibId: str
    brn: int
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
    titles: List[Dict[str, Any]] = []
    if isinstance(response, dict):
        if isinstance(response.get("Result"), dict):
            titles = response["Result"].get("Titles") or []
        if not titles:
            titles = response.get("titles") or []
    normalized: List[TitleSummary] = []
    for item in titles:
        # Support both camelCase/caps variants from the API.
        title = item.get("title") or item.get("TitleName")
        author = item.get("author") or item.get("AuthorName")
        isbn = item.get("isbn") or item.get("ISBN")
        # Prefer explicit bibId; fall back to BRN if present.
        bib_id = item.get("bibId") or item.get("BID")
        brn = item.get("brn") or item.get("BRN")
        if not bib_id and brn is not None:
            try:
                bib_id = str(brn)
            except Exception:
                pass

        publisher = item.get("publisher") or item.get("Publisher")
        publish_year = item.get("publishYear") or item.get("PublishYear")
        category = item.get("Category") or item.get("format")
        subjects = item.get("subjects") or item.get("Subjects") or []
        if subjects is None:
            subjects = []

        entry: TitleSummary = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "bibId": bib_id,
            "brn": brn,
            "publisher": publisher,
            "publishYear": publish_year,
            "formats": [category] if category else [],
            "subjects": subjects,
        }
        normalized.append(_strip_nones(entry))
    return normalized


def normalize_availability(response: Dict[str, Any]) -> List[NormalizedAvailability]:
    items: List[Dict[str, Any]] = []
    if isinstance(response, dict):
        if isinstance(response.get("Result"), dict):
            items = response["Result"].get("Items") or []
        if not items:
            items = response.get("items") or []
    normalized: List[NormalizedAvailability] = []
    for item in items:
        branch = (
            item.get("branchName")
            or item.get("BranchName")
            or item.get("branchId")
            or item.get("BranchID")
            or "Unknown branch"
        )
        call_number = item.get("callNumber") or item.get("CallNumber")
        status = item.get("status") or item.get("Status")
        available = item.get("available") if "available" in item else item.get("Available")
        total = item.get("total") if "total" in item else item.get("Total")

        entry: NormalizedAvailability = {
            "branch": branch,
            "callNumber": call_number,
            "status": status,
            "available": available,
            "total": total,
        }
        normalized.append(_strip_nones(entry))
    return normalized


def _strip_nones(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy without None values to satisfy strict JSON schema validators."""
    return {k: v for k, v in obj.items() if v is not None}
