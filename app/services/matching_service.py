from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from app.adapters.flights_base import BaseFlightAdapter
from app.adapters.transfers_base import BaseTransferAdapter
from app.config import Settings
from app.models import AccommodationOption, Destination, TripDateOption, TripResult
from app.services.filter_service import (
    accommodation_matches_requirements,
    flight_matches_requirements,
    trip_within_budget,
)
from app.services.scoring_service import calculate_accommodation_quality_score


def build_trip_results(
    destination: Destination,
    date_option: TripDateOption,
    stays: list[AccommodationOption],
    flight_adapter: BaseFlightAdapter,
    transfer_adapter: BaseTransferAdapter,
    settings: Settings,
) -> list[TripResult]:
    filtered_stays = [s for s in stays if accommodation_matches_requirements(s, settings)]
    filtered_stays.sort(key=lambda s: s.total_price + s.booking_fee)

    results: list[TripResult] = []
    search_timestamp = datetime.now(ZoneInfo(settings.timezone_name))

    for stay in filtered_stays:
        stay_total = round(stay.total_price + stay.booking_fee, 2)
        if stay_total >= settings.total_budget:
            continue

        flights = flight_adapter.search_flights(
            origin=settings.departure_airport,
            destination=destination.arrival_airport,
            departure_date=date_option.departure_date,
            return_date=date_option.return_date,
            adults=settings.adults,
            direct_only=settings.direct_flights_only,
            checked_bags_total=settings.checked_bags_total,
        )

        valid_flights = [f for f in flights if flight_matches_requirements(f, settings)]
        valid_flights.sort(key=lambda f: f.total_price)

        if not valid_flights:
            continue

        transfer = transfer_adapter.get_transfer_cost(destination.arrival_airport, stay)

        for flight in valid_flights:
            trip_total = round(stay_total + flight.total_price + transfer.total_price, 2)
            if not trip_within_budget(trip_total, settings.total_budget):
                continue

            quality_score = calculate_accommodation_quality_score(stay)

            results.append(
                TripResult(
                    search_timestamp=search_timestamp,
                    destination_city=destination.city,
                    destination_country=destination.country,
                    arrival_airport=destination.arrival_airport,
                    departure_date=date_option.departure_date,
                    return_date=date_option.return_date,
                    nights=date_option.nights,
                    flight=flight,
                    accommodation=stay,
                    transfer=transfer,
                    trip_total=trip_total,
                    trip_total_per_person=round(trip_total / settings.adults, 2),
                    accommodation_quality_score=quality_score,
                    destination_fit_score=destination.fit_score,
                    price_score=0.0,
                    value_score=0.0,
                )
            )

    return results
