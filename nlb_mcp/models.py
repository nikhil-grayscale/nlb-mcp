"""Lightweight response and normalized types."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class FacetData(TypedDict, total=False):
    id: str
    data: str
    count: int


class Facet(TypedDict, total=False):
    id: str
    name: str
    values: List[FacetData]


class TitleRecord(TypedDict, total=False):
    brn: int
    digitalId: str
    isbn: str
    publisher: str
    summary: str
    allowReservation: bool
    activeReservations: int
    language: str
    volume: str
    availability: Any
    otherTitles: List[str]
    nativeOtherTitles: List[str]
    variantTitles: List[str]
    nativeVariantTitles: List[str]
    otherAuthors: List[str]
    nativeOtherAuthors: List[str]
    subjects: List[str]
    format: str
    materialType: str


class TitleSummary(TypedDict, total=False):
    title: str
    nativeTitle: str
    seriesTitle: List[str]
    nativeSeriesTitle: List[str]
    author: str
    nativeAuthor: str
    coverUrl: Dict[str, Any]
    records: List[TitleRecord]


class NormalizedAvailability(TypedDict, total=False):
    branch: str
    callNumber: str
    status: str
    available: int
    total: int


def normalize_titles(response: Dict[str, Any]) -> Dict[str, Any]:
    titles_raw: List[Dict[str, Any]] = []
    facets = []
    total_records = None
    count = None
    has_more = None
    next_offset = None

    if isinstance(response, dict):
        if "Result" in response and isinstance(response["Result"], dict):
            result = response["Result"]
            titles_raw = result.get("Titles") or []
            total_records = result.get("TotalRecords")
            count = result.get("Count") or result.get("count")
            has_more = result.get("HasMoreRecords")
            next_offset = result.get("NextRecordsOffset")
        else:
            titles_raw = response.get("titles") or []
            total_records = response.get("totalRecords")
            count = response.get("count")
            has_more = response.get("hasMoreRecords")
            next_offset = response.get("nextRecordsOffset")
        facets = response.get("facets") or response.get("Facets") or []

    titles: List[TitleSummary] = []
    for item in titles_raw:
        title = item.get("title") or item.get("TitleName")
        native_title = item.get("nativeTitle")
        series_title = item.get("seriesTitle") or []
        native_series_title = item.get("nativeSeriesTitle") or []
        author = item.get("author") or item.get("AuthorName")
        native_author = item.get("nativeAuthor")
        cover_url = item.get("coverUrl") or {}
        records = _normalize_records(item.get("records") or item.get("Records"))

        entry: TitleSummary = {
            "title": title,
            "nativeTitle": native_title,
            "seriesTitle": series_title if isinstance(series_title, list) else [],
            "nativeSeriesTitle": native_series_title if isinstance(native_series_title, list) else [],
            "author": author,
            "nativeAuthor": native_author,
            "coverUrl": cover_url if isinstance(cover_url, dict) else {},
            "records": records,
        }
        titles.append(_strip_nones(entry))

    return _strip_nones(
        {
            "totalRecords": total_records,
            "count": count,
            "hasMoreRecords": has_more,
            "nextRecordsOffset": next_offset,
            "titles": titles,
            "facets": _normalize_facets(facets),
        }
    )


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


def _extract_brn_from_records(item: Dict[str, Any]) -> Any:
    records = item.get("records") or item.get("Records")
    if not isinstance(records, list) or not records:
        return None
    first = records[0]
    if not isinstance(first, dict):
        return None
    return first.get("brn") or first.get("BRN")


def _normalize_records(records: Any) -> List[Dict[str, Any]]:
    if not isinstance(records, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        normalized.append(
            _strip_nones(
                {
                    "brn": rec.get("brn") or rec.get("BRN"),
                    "digitalId": rec.get("digitalId") or rec.get("DigitalId") or rec.get("DigitalID"),
                    "isbn": rec.get("isbn") or rec.get("ISBN"),
                    "publisher": rec.get("publisher") or rec.get("Publisher"),
                    "summary": rec.get("summary") or rec.get("Summary"),
                    "allowReservation": rec.get("allowReservation") or rec.get("AllowReservation"),
                    "activeReservations": rec.get("activeReservations") or rec.get("ActiveReservations"),
                    "language": rec.get("language") or rec.get("Language"),
                    "volume": rec.get("volume") or rec.get("Volume"),
                    "availability": rec.get("availability") or rec.get("Availability"),
                    "otherTitles": rec.get("otherTitles") or rec.get("OtherTitles") or [],
                    "nativeOtherTitles": rec.get("nativeOtherTitles") or rec.get("NativeOtherTitles") or [],
                    "variantTitles": rec.get("variantTitles") or rec.get("VariantTitles") or [],
                    "nativeVariantTitles": rec.get("nativeVariantTitles") or rec.get("NativeVariantTitles") or [],
                    "otherAuthors": rec.get("otherAuthors") or rec.get("OtherAuthors") or [],
                    "nativeOtherAuthors": rec.get("nativeOtherAuthors") or rec.get("NativeOtherAuthors") or [],
                    "subjects": rec.get("subjects") or rec.get("Subjects") or [],
                    "format": rec.get("format") or rec.get("Format"),
                    "materialType": rec.get("materialType") or rec.get("MaterialType"),
                }
            )
        )
    return normalized


def _normalize_facets(facets: Any) -> List[Facet]:
    if not isinstance(facets, list):
        return []
    normalized: List[Facet] = []
    for fac in facets:
        if not isinstance(fac, dict):
            continue
        values_raw = fac.get("values") or fac.get("Values") or []
        values: List[FacetData] = []
        if isinstance(values_raw, list):
            for val in values_raw:
                if not isinstance(val, dict):
                    continue
                values.append(
                    _strip_nones(
                        {
                            "id": val.get("id") or val.get("Id"),
                            "data": val.get("data") or val.get("Data"),
                            "count": val.get("count") or val.get("Count"),
                        }
                    )
                )
        normalized.append(
            _strip_nones(
                {
                    "id": fac.get("id") or fac.get("Id"),
                    "name": fac.get("name") or fac.get("Name"),
                    "values": values,
                }
            )
        )
    return normalized


def _normalize_records(records: Any) -> List[Dict[str, Any]]:
    if not isinstance(records, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        normalized.append(
            _strip_nones(
                {
                    "brn": rec.get("brn") or rec.get("BRN"),
                    "digitalId": rec.get("digitalId") or rec.get("DigitalId") or rec.get("DigitalID"),
                    "otherTitles": rec.get("otherTitles") or rec.get("OtherTitles") or [],
                    "nativeOtherTitles": rec.get("nativeOtherTitles") or rec.get("NativeOtherTitles") or [],
                    "variantTitles": rec.get("variantTitles") or rec.get("VariantTitles") or [],
                    "nativeVariantTitles": rec.get("nativeVariantTitles") or rec.get("NativeVariantTitles") or [],
                    "otherAuthors": rec.get("otherAuthors") or rec.get("OtherAuthors") or [],
                    "nativeOtherAuthors": rec.get("nativeOtherAuthors") or rec.get("NativeOtherAuthors") or [],
                    "subjects": rec.get("subjects") or rec.get("Subjects") or [],
                    "format": rec.get("format") or rec.get("Format"),
                    "materialType": rec.get("materialType") or rec.get("MaterialType"),
                }
            )
        )
    return normalized
