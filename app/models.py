from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass(frozen=True)
class Destination:
    code: str
    city: str
    country: str
    arrival_airport: str
    fit_score: float
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class TripDateOption:
    departure_date: date
    return_date: date
    nights: int


@dataclass(frozen=True)
class FlightOption:
    origin: str
    destination: str
    departure_date: date
    return_date: date
    airline: str
    is_direct: bool
    adults: int
    base_price: float
    bag_fee: float
    booking_fee: float
    total_price: float
    checked_bag_included: bool
    source: str
    url: Optional[str] = None


@dataclass(frozen=True)
class AccommodationOption:
    property_name: str
    destination_code: str
    property_type: str
    checkin: date
    checkout: date
    nights: int
    adults: int
    total_price: float
    booking_fee: float
    private_bathroom: bool
    bed_type: str
    hotel_stars: Optional[float]
    review_score_5: Optional[float]
    review_score_10: Optional[float]
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: str = ""
    url: Optional[str] = None


@dataclass(frozen=True)
class TransferOption:
    arrival_airport: str
    estimated: bool
    arrival_transfer_cost: float
    departure_transfer_cost: float
    total_price: float
    source: str


@dataclass
class TripResult:
    search_timestamp: datetime
    destination_city: str
    destination_country: str
    arrival_airport: str
    departure_date: date
    return_date: date
    nights: int
    flight: FlightOption
    accommodation: AccommodationOption
    transfer: TransferOption
    trip_total: float
    trip_total_per_person: float
    accommodation_quality_score: float
    destination_fit_score: float
    price_score: float
    value_score: float
    rank: Optional[int] = None
