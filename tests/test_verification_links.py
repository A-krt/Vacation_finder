from app.services.verification_links import (
    build_booking_verification_url,
    build_expedia_verification_url,
    build_google_flights_verification_url,
    build_google_hotels_verification_url,
)


def test_booking_verification_url_contains_destination() -> None:
    url = build_booking_verification_url("Alicante", "2026-07-01", "2026-07-10", 2)
    assert "Alicante" in url
    assert "checkin=2026-07-01" in url


def test_expedia_verification_url_contains_dates() -> None:
    url = build_expedia_verification_url("Alicante", "2026-07-01", "2026-07-10", 2)
    assert "startDate=2026-07-01" in url
    assert "endDate=2026-07-10" in url


def test_google_links_are_created() -> None:
    flight_url = build_google_flights_verification_url("AMS", "Alicante", "2026-07-01", "2026-07-10", 2)
    hotel_url = build_google_hotels_verification_url("Alicante", "2026-07-01", "2026-07-10")

    assert "google.com" in flight_url
    assert "google.com" in hotel_url
