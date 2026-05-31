from __future__ import annotations

from app.adapters.flights_base import BaseFlightAdapter
from app.adapters.stays_base import BaseStayAdapter
from app.adapters.transfers_base import BaseTransferAdapter
from app.config import get_settings
from app.destinations.seed_list import DESTINATIONS
from app.generators.date_generator import generate_trip_date_options
from app.models import TripResult
from app.services.matching_service import build_trip_results
from app.services.scoring_service import calculate_price_score, calculate_value_score
from app.utils.logger import get_logger


logger = get_logger(__name__)


def run_search(
    flight_adapter: BaseFlightAdapter,
    stay_adapter: BaseStayAdapter,
    transfer_adapter: BaseTransferAdapter,
) -> list[TripResult]:
    settings = get_settings()
    date_options = generate_trip_date_options(settings.allowed_departure_months, settings.nights_options)

    logger.info(
        "Zoekrun gestart met %s bestemmingen en %s datumopties",
        len(DESTINATIONS),
        len(date_options),
    )

    results: list[TripResult] = []

    for destination in DESTINATIONS:
        for date_option in date_options:
            stays = stay_adapter.search_stays(
                destination_code=destination.arrival_airport,
                checkin=date_option.departure_date,
                checkout=date_option.return_date,
                adults=settings.adults,
            )

            if not stays:
                continue

            results.extend(
                build_trip_results(
                    destination=destination,
                    date_option=date_option,
                    stays=stays,
                    flight_adapter=flight_adapter,
                    transfer_adapter=transfer_adapter,
                    settings=settings,
                )
            )

    if not results:
        logger.warning("Geen geldige reizen gevonden binnen het budget.")
        return []

    min_total = min(r.trip_total for r in results)
    max_total = max(r.trip_total for r in results)

    for result in results:
        result.price_score = calculate_price_score(result.trip_total, min_total, max_total)
        result.value_score = calculate_value_score(
            price_score=result.price_score,
            accommodation_quality_score=result.accommodation_quality_score,
            destination_fit_score=result.destination_fit_score,
            weights=settings.ranking_weights,
        )

    results.sort(
        key=lambda r: (
            -r.value_score,
            r.trip_total,
            -r.accommodation_quality_score,
            -r.destination_fit_score,
        )
    )

    for idx, result in enumerate(results, start=1):
        result.rank = idx

    logger.info("Zoekrun afgerond met %s geldige reizen", len(results))
    return results
