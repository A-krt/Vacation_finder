from __future__ import annotationsfrom __future__ import annotations, urlencode

from app.models import TripResult
from app.utils.csv_utils import write_csv_rows


def build_booking_verification_url(destination_city: str, checkin: str, checkout: str, adults: int) -> str:
    params = {
        "ss": destination_city,
        "checkin": checkin,
        "checkout": checkout,
        "group_adults": adults,
        "no_rooms": 1,
        "group_children": 0,
        "selected_currency": "EUR",
    }
    return f"https://www.booking.com/searchresults.html?{urlencode(params)}"


def build_expedia_verification_url(destination_city: str, checkin: str, checkout: str, adults: int) -> str:
    params = {
        "destination": destination_city,
        "startDate": checkin,
        "endDate": checkout,
        "rooms": 1,
        "adults": adults,
    }
    return f"https://www.expedia.com/Hotel-Search?{urlencode(params)}"


def build_google_hotels_verification_url(destination_city: str, checkin: str, checkout: str) -> str:
    query = f"{destination_city} hotels {checkin} {checkout}"
    return f"https://www.google.com/travel/hotels?hl=en&q={quote_plus(query)}"


def build_google_flights_verification_url(
    departure_airport: str,
    destination_city: str,
    checkin: str,
    checkout: str,
    adults: int,
) -> str:
    query = f"{departure_airport} {destination_city} flights {checkin} {checkout} {adults} adults"
    return f"https://www.google.com/search?q={quote_plus(query)}"


def build_google_maps_verification_url(property_name: str, destination_city: str) -> str:
    query = f"{property_name} {destination_city}"
    return f"https://www.google.com/maps/search/{quote_plus(query)}"


def create_shortlist_rows(results: list[TripResult], top_n: int) -> list[dict]:
    rows: list[dict] = []

    for result in results[:top_n]:
        rows.append(
            {
                "rank": result.rank,
                "destination": result.destination_city,
                "destination_country": result.destination_country,
                "departure_date": result.departure_date.isoformat(),
                "return_date": result.return_date.isoformat(),
                "nights": result.nights,
                "property_name": result.accommodation.property_name,
                "property_type": result.accommodation.property_type,
                "flight_total": result.flight.total_price,
                "stay_total": round(result.accommodation.total_price + result.accommodation.booking_fee, 2),
                "transfer_total": result.transfer.total_price,
                "trip_total": result.trip_total,
                "trip_total_per_person": result.trip_total_per_person,
                "accommodation_quality_score": result.accommodation_quality_score,
                "destination_fit_score": result.destination_fit_score,
                "price_score": result.price_score,
                "value_score": result.value_score,
                "stay_source": result.accommodation.source,
                "flight_source": result.flight.source,
            }
        )

    return rows


def create_verification_rows(results: list[TripResult], top_n: int) -> list[dict]:
    rows: list[dict] = []

    for result in results[:top_n]:
        checkin = result.departure_date.isoformat()
        checkout = result.return_date.isoformat()

        rows.append(
            {
                "rank": result.rank,
                "destination": result.destination_city,
                "destination_country": result.destination_country,
                "departure_airport": result.flight.origin,
                "departure_date": checkin,
                "return_date": checkout,
                "nights": result.nights,
                "property_name": result.accommodation.property_name,
                "trip_total": result.trip_total,
                "trip_total_per_person": result.trip_total_per_person,
                "value_score": result.value_score,
                "booking_verification_url": build_booking_verification_url(
                    result.destination_city,
                    checkin,
                    checkout,
                    result.flight.adults,
                ),
                "expedia_verification_url": build_expedia_verification_url(
                    result.destination_city,
                    checkin,
                    checkout,
                    result.flight.adults,
                ),
                "google_hotels_verification_url": build_google_hotels_verification_url(
                    result.destination_city,
                    checkin,
                    checkout,
                ),
                "google_flights_verification_url": build_google_flights_verification_url(
                    result.flight.origin,
                    result.destination_city,
                    checkin,
                    checkout,
                    result.flight.adults,
                ),
                "google_maps_property_url": build_google_maps_verification_url(
                    result.accommodation.property_name,
                    result.destination_city,
                ),
            }
        )

    return rows


def export_shortlist_to_csv(rows: list[dict], output_path: Path | str) -> str:
    return write_csv_rows(rows, Path(output_path))


def export_verification_links_to_csv(rows: list[dict], output_path: Path | str) -> str:
    return write_csv_rows(rows, Path(output_path))
``

from pathlib import Path
