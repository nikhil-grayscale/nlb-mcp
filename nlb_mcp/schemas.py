"""Typed schemas auto-derived from swagger."""
from __future__ import annotations
from typing import Any, Dict, List, TypedDict

class BadRequestError(TypedDict, total=False):
    statusCode: int
    error: str
    message: str

class BibFormat(TypedDict, total=False):
    code: str
    name: str

class BookCover(TypedDict, total=False):
    small: str
    medium: str
    large: str

class CheckoutsTitle(TypedDict, total=False):
    title: str
    nativeTitle: str
    author: str
    nativeAuthor: str
    isbns: List[str]
    checkoutsCount: int

class CheckoutsTrend(TypedDict, total=False):
    language: str
    ageLevel: str
    fiction: bool
    singaporeCollection: bool
    checkoutsTitles: List[CheckoutsTitle]

class CourseCode(TypedDict, total=False):
    code: str
    clusterName: str
    categoryName: str

class Facet(TypedDict, total=False):
    id: str
    name: str
    values: List[FacetData]

class FacetData(TypedDict, total=False):
    id: str
    data: str
    count: int

class GetAvailabilityInfoResponseV2(TypedDict, total=False):
    setId: int
    totalRecords: int
    count: int
    hasMoreRecords: bool
    nextRecordsOffset: int
    items: List[Item]

class GetTitleDetailsResponseV2(TypedDict, total=False):
    brn: int
    digitalId: str
    otherTitles: List[str]
    nativeOtherTitles: List[str]
    variantTitles: List[str]
    nativeVariantTitles: List[str]
    otherAuthors: List[str]
    nativeOtherAuthors: List[str]
    isbns: List[str]
    issns: List[str]
    format: BibFormat
    edition: List[str]
    nativeEdition: List[str]
    publisher: List[str]
    nativePublisher: List[str]
    publishDate: str
    subjects: List[str]
    physicalDescription: List[str]
    nativePhysicalDescription: List[str]
    summary: List[str]
    nativeSummary: List[str]
    contents: List[str]
    nativeContents: List[str]
    thesis: List[str]
    nativeThesis: List[str]
    notes: List[str]
    nativeNotes: List[str]
    allowReservation: bool
    isRestricted: bool
    activeReservationsCount: int
    audience: List[str]
    audienceImda: List[str]
    language: List[str]
    serial: bool
    volumeNote: List[str]
    nativeVolumeNote: List[str]
    frequency: List[str]
    nativeFrequency: List[str]
    credits: List[str]
    nativeCredits: List[str]
    performers: List[str]
    nativePerformers: List[str]
    availability: bool
    source: str
    volumes: List[str]
    title: str
    nativeTitle: str
    seriesTitle: List[str]
    nativeSeriesTitle: List[str]
    author: str
    nativeAuthor: str

class GetTitlesResponseV2(TypedDict, total=False):
    totalRecords: int
    count: int
    hasMoreRecords: bool
    nextRecordsOffset: int
    setId: int
    titles: List[Title]

class InternalServerError(TypedDict, total=False):
    statusCode: int
    error: str
    message: str

class Item(TypedDict, total=False):
    irn: int
    itemId: str
    brn: int
    volumeName: str
    callNumber: str
    formattedCallNumber: str
    media: Media
    usageLevel: UsageLevel
    location: Location
    courseCode: CourseCode
    language: str
    suffix: str
    donor: str
    price: float
    status: Status
    transactionStatus: TransactionStatus
    minAgeLimit: int

class Location(TypedDict, total=False):
    code: str
    name: str

class Media(TypedDict, total=False):
    code: str
    name: str

class MethodNotAllowedError(TypedDict, total=False):
    statusCode: int
    error: str
    message: str

class NewArrivalTitle(TypedDict, total=False):
    brn: int
    digitalId: str
    otherTitles: List[str]
    nativeOtherTitles: List[str]
    variantTitles: List[str]
    nativeVariantTitles: List[str]
    otherAuthors: List[str]
    nativeOtherAuthors: List[str]
    isbns: List[str]
    issns: List[str]
    format: BibFormat
    edition: List[str]
    nativeEdition: List[str]
    publisher: List[str]
    nativePublisher: List[str]
    publishDate: str
    subjects: List[str]
    physicalDescription: List[str]
    nativePhysicalDescription: List[str]
    summary: List[str]
    nativeSummary: List[str]
    contents: List[str]
    nativeContents: List[str]
    thesis: List[str]
    nativeThesis: List[str]
    notes: List[str]
    nativeNotes: List[str]
    allowReservation: bool
    isRestricted: bool
    activeReservationsCount: int
    audience: List[str]
    audienceImda: List[str]
    language: List[str]
    serial: bool
    volumeNote: List[str]
    nativeVolumeNote: List[str]
    frequency: List[str]
    nativeFrequency: List[str]
    credits: List[str]
    nativeCredits: List[str]
    performers: List[str]
    nativePerformers: List[str]
    availability: bool
    source: str
    volumes: List[str]
    title: str
    nativeTitle: str
    seriesTitle: List[str]
    nativeSeriesTitle: List[str]
    author: str
    nativeAuthor: str

class NotFoundError(TypedDict, total=False):
    statusCode: int
    error: str
    message: str

class NotImplementedError(TypedDict, total=False):
    statusCode: int
    error: str
    message: str

class SearchMostCheckoutsTitlesResponse(TypedDict, total=False):
    checkoutsTrends: List[CheckoutsTrend]

class SearchNewTitlesResponseV2(TypedDict, total=False):
    totalRecords: int
    count: int
    nextRecordsOffset: int
    hasMoreRecords: bool
    titles: List[NewArrivalTitle]

class SearchTitlesResponseV2(TypedDict, total=False):
    totalRecords: int
    count: int
    hasMoreRecords: bool
    nextRecordsOffset: int
    titles: List[TitleSummary]
    facets: List[Facet]

class ServiceUnavailableError(TypedDict, total=False):
    statusCode: int
    error: str
    message: str

class Status(TypedDict, total=False):
    code: str
    name: str
    setDate: str

class Title(TypedDict, total=False):
    brn: int
    digitalId: str
    otherTitles: List[str]
    nativeOtherTitles: List[str]
    variantTitles: List[str]
    nativeVariantTitles: List[str]
    otherAuthors: List[str]
    nativeOtherAuthors: List[str]
    isbns: List[str]
    issns: List[str]
    format: BibFormat
    edition: List[str]
    nativeEdition: List[str]
    publisher: List[str]
    nativePublisher: List[str]
    publishDate: str
    subjects: List[str]
    physicalDescription: List[str]
    nativePhysicalDescription: List[str]
    summary: List[str]
    nativeSummary: List[str]
    contents: List[str]
    nativeContents: List[str]
    thesis: List[str]
    nativeThesis: List[str]
    notes: List[str]
    nativeNotes: List[str]
    allowReservation: bool
    isRestricted: bool
    activeReservationsCount: int
    audience: List[str]
    audienceImda: List[str]
    language: List[str]
    serial: bool
    volumeNote: List[str]
    nativeVolumeNote: List[str]
    frequency: List[str]
    nativeFrequency: List[str]
    credits: List[str]
    nativeCredits: List[str]
    performers: List[str]
    nativePerformers: List[str]
    availability: bool
    source: str
    volumes: List[str]
    title: str
    nativeTitle: str
    seriesTitle: List[str]
    nativeSeriesTitle: List[str]
    author: str
    nativeAuthor: str

class TitleRecord(TypedDict, total=False):
    brn: int
    digitalId: str
    otherTitles: List[str]
    nativeOtherTitles: List[str]
    variantTitles: List[str]
    nativeVariantTitles: List[str]
    otherAuthors: List[str]
    nativeOtherAuthors: List[str]
    isbns: List[str]
    issns: List[str]
    format: BibFormat
    edition: List[str]
    nativeEdition: List[str]
    publisher: List[str]
    nativePublisher: List[str]
    publishDate: str
    subjects: List[str]
    physicalDescription: List[str]
    nativePhysicalDescription: List[str]
    summary: List[str]
    nativeSummary: List[str]
    contents: List[str]
    nativeContents: List[str]
    thesis: List[str]
    nativeThesis: List[str]
    notes: List[str]
    nativeNotes: List[str]
    allowReservation: bool
    isRestricted: bool
    activeReservationsCount: int
    audience: List[str]
    audienceImda: List[str]
    language: List[str]
    serial: bool
    volumeNote: List[str]
    nativeVolumeNote: List[str]
    frequency: List[str]
    nativeFrequency: List[str]
    credits: List[str]
    nativeCredits: List[str]
    performers: List[str]
    nativePerformers: List[str]
    availability: bool
    source: str
    volumes: List[str]

class TitleSummary(TypedDict, total=False):
    title: str
    nativeTitle: str
    seriesTitle: List[str]
    nativeSeriesTitle: List[str]
    author: str
    nativeAuthor: str
    coverUrl: BookCover
    records: List[TitleRecord]

class TooManyRequestsError(TypedDict, total=False):
    statusCode: int
    error: str
    message: str

class TransactionStatus(TypedDict, total=False):
    code: str
    name: str
    date: str
    inTransitFrom: Location
    inTransitTo: Location

class UnauthorizedError(TypedDict, total=False):
    statusCode: int
    error: str
    message: str

class UsageLevel(TypedDict, total=False):
    code: str
    name: str
