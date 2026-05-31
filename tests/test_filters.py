from datetime import date

from app.config import get_settings
from app.models import AccommodationOption, FlightOption
from app.services.filter_service import accommodation_matches_requirements, flight_matches_requirements


SETTINGS = get_settings()


def test_accommodation_or_quality_filter_passes() -> None:
    acc = AccommodationOption(
        property_name="Test Stay",
        destination_code="ALC",
        property_type="apartment",
        checkin=date(2026, 7, 1),
        checkout=date(2026, 7, 10),
        nights=9,
        adults=2,
        total_price=800.0,
        booking_fee=15.0,
        private_bathroom=True,
        bed_type="double",
        hotel_stars=None,
        review_score_5=4.1,
        review_score_10=None,
    )
    assert accommodation_matches_requirements(acc, SETTINGS)


def test_flight_filter_passes_for_direct_with_bag() -> None:
    flight = FlightOption(
        origin="AMS",
        destination="ALC",
        departure_date=date(2026, 7, 1),
        return_date=date(2026, 7, 10),
        airline="KLM",
        is_direct=True,
        adults=2,
        base_price=300.0,
        bag_fee=55.0,
        booking_fee=14.0,
        total_price=369.0,
        checked_bag_included=True,
        source="test",
    )
    assert flight_matches_requirements(flight, SETTINGS)
