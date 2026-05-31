from __future__ import annotations

from app.config import Settings
from app.models import AccommodationOption, FlightOption


def accommodation_matches_requirements(accommodation: AccommodationOption, settings: Settings) -> bool:
    if accommodation.property_type not in settings.allowed_accommodation_types:
        return False
    if settings.require_private_bathroom and not accommodation.private_bathroom:
        return False
    if accommodation.bed_type != settings.require_bed_type:
        return False

    quality_ok = (
        (accommodation.hotel_stars is not None and accommodation.hotel_stars >= settings.min_hotel_stars)
        or (accommodation.review_score_5 is not None and accommodation.review_score_5 >= settings.min_review_5)
        or (accommodation.review_score_10 is not None and accommodation.review_score_10 >= settings.min_review_10)
    )
    return quality_ok


def flight_matches_requirements(flight: FlightOption, settings: Settings) -> bool:
    if settings.direct_flights_only and not flight.is_direct:
        return False
    if flight.adults != settings.adults:
        return False
    if settings.checked_bags_total >= 1 and not flight.checked_bag_included:
        return False
    return True


def trip_within_budget(total_price: float, max_total: float) -> bool:
    return total_price <= max_total
