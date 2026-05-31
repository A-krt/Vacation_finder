from datetime import date

from app.models import AccommodationOption
from app.services.scoring_service import (
    calculate_accommodation_quality_score,
    calculate_price_score,
    calculate_value_score,
)


def test_calculate_accommodation_quality_score() -> None:
    acc = AccommodationOption(
        property_name="Test",
        destination_code="ALC",
        property_type="hotel",
        checkin=date(2026, 7, 1),
        checkout=date(2026, 7, 10),
        nights=9,
        adults=2,
        total_price=900.0,
        booking_fee=15.0,
        private_bathroom=True,
        bed_type="double",
        hotel_stars=4.0,
        review_score_5=None,
        review_score_10=None,
    )
    assert calculate_accommodation_quality_score(acc) == 8.0


def test_calculate_price_score_and_value() -> None:
    price_score = calculate_price_score(1000.0, 900.0, 1500.0)
    assert 0 <= price_score <= 10

    value = calculate_value_score(
        price_score,
        8.5,
        8.8,
        {"price": 0.4, "quality": 0.35, "destination_fit": 0.25},
    )
    assert value > 0
