from __future__ import annotations

from app.models import AccommodationOption
from app.services.normalization_service import get_best_quality_score


def calculate_accommodation_quality_score(accommodation: AccommodationOption) -> float:
    score = get_best_quality_score(
        hotel_stars=accommodation.hotel_stars,
        review_5=accommodation.review_score_5,
        review_10=accommodation.review_score_10,
    )
    return round(score if score is not None else 0.0, 2)


def calculate_price_score(trip_total: float, min_total: float, max_total: float) -> float:
    if max_total <= min_total:
        return 10.0
    normalized = (max_total - trip_total) / (max_total - min_total)
    normalized = min(1.0, max(0.0, normalized))
    return round(normalized * 10.0, 2)


def calculate_value_score(
    price_score: float,
    accommodation_quality_score: float,
    destination_fit_score: float,
    weights: dict[str, float],
) -> float:
    value = (
        weights["price"] * price_score
        + weights["quality"] * accommodation_quality_score
        + weights["destination_fit"] * destination_fit_score
    )
    return round(value, 4)
