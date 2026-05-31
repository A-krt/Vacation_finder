from __future__ import annotations

from datetime import date

import requests

from app.adapters.flights_base import BaseFlightAdapter
from app.config import Settings, get_settings
from app.models import FlightOption
from app.utils.logger import get_logger


logger = get_logger(__name__)


class SerpApiFlightAdapter(BaseFlightAdapter):
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        if not self.settings.serpapi_api_key:
            raise RuntimeError("SERPAPI_API_KEY ontbreekt")

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: date,
        return_date: date,
        adults: int,
        direct_only: bool,
        checked_bags_total: int,
    ) -> list[FlightOption]:
        params = {
            "engine": "google_flights",
            "api_key": self.settings.serpapi_api_key,
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": departure_date.isoformat(),
            "return_date": return_date.isoformat(),
            "adults": adults,
            "type": 1,
            "currency": self.settings.serpapi_currency,
            "hl": self.settings.serpapi_language,
            "gl": self.settings.serpapi_country,
        }

        response = requests.get(
            "https://serpapi.com/search.json",
            params=params,
            timeout=self.settings.serpapi_timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()

        itineraries = []
        itineraries.extend(payload.get("best_flights", []))
        itineraries.extend(payload.get("other_flights", []))

        options: list[FlightOption] = []

        for item in itineraries[: self.settings.provider_max_results]:
            flights = item.get("flights", [])
            if not flights:
                continue

            is_direct = len(flights) == 2 or len(item.get("layovers", [])) == 0
            if direct_only and not is_direct:
                continue

            airline = flights[0].get("airline", "Unknown airline")
            base_price = float(item.get("price") or 0.0)

            # To stay within free-tier limits, baggage is estimated instead of fetched via extra booking-option calls.
            bag_fee = self.settings.checked_bag_fee_estimate_total if checked_bags_total > 0 else 0.0
            booking_fee = 0.0
            total_price = round(base_price + bag_fee + booking_fee, 2)

            options.append(
                FlightOption(
                    origin=origin,
                    destination=destination,
                    departure_date=departure_date,
                    return_date=return_date,
                    airline=airline,
                    is_direct=is_direct,
                    adults=adults,
                    base_price=base_price,
                    bag_fee=bag_fee,
                    booking_fee=booking_fee,
                    total_price=total_price,
                    checked_bag_included=checked_bags_total == 0,
                    source="serpapi_google_flights",
                )
            )

        logger.info("SerpApi flights gaf %s opties voor %s -> %s", len(options), origin, destination)
        return options
``
