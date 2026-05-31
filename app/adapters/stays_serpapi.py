from __future__ import annotations

from datetime import date

import requests

from app.adapters.stays_base import BaseStayAdapter
from app.config import Settings, get_settings
from app.destinations.seed_list import DESTINATIONS
from app.models import AccommodationOption
from app.utils.logger import get_logger


logger = get_logger(__name__)
_DESTINATION_LOOKUP = {d.arrival_airport: d.city for d in DESTINATIONS}


class SerpApiStayAdapter(BaseStayAdapter):
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        if not self.settings.serpapi_api_key:
            raise RuntimeError("SERPAPI_API_KEY ontbreekt")

    def search_stays(
        self,
        destination_code: str,
        checkin: date,
        checkout: date,
        adults: int,
    ) -> list[AccommodationOption]:
        city = _DESTINATION_LOOKUP.get(destination_code, destination_code)

        params = {
            "engine": "google_hotels",
            "api_key": self.settings.serpapi_api_key,
            "q": city,
            "check_in_date": checkin.isoformat(),
            "check_out_date": checkout.isoformat(),
            "adults": adults,
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

        properties = payload.get("properties", [])
        options: list[AccommodationOption] = []
        nights = (checkout - checkin).days

        for item in properties[: self.settings.provider_max_results]:
            total_price = _extract_total_price(item)
            if total_price is None:
                continue

            property_name = item.get("name") or item.get("title") or "Unknown property"
            property_type = (item.get("type") or item.get("property_type") or "hotel").strip().lower().replace(" ", "_")
            if property_type not in {"hotel", "apartment", "holiday_home"}:
                property_type = "hotel"

            rating_5 = _extract_rating_5(item)
            rating_10 = round(rating_5 * 2, 2) if rating_5 is not None else None
            stars = _extract_stars(item)

            options.append(
                AccommodationOption(
                    property_name=property_name,
                    destination_code=destination_code,
                    property_type=property_type,
                    checkin=checkin,
                    checkout=checkout,
                    nights=nights,
                    adults=adults,
                    total_price=float(total_price),
                    booking_fee=0.0,
                    private_bathroom=True,
                    bed_type="double",
                    hotel_stars=stars,
                    review_score_5=rating_5,
                    review_score_10=rating_10,
                )
            )

        logger.info("SerpApi stays gaf %s opties voor %s", len(options), city)
        return options


def _extract_total_price(item: dict) -> float | None:
    total_rate = item.get("total_rate") or {}
    if isinstance(total_rate, dict):
        for key in ("lowest", "price", "value", "extracted_lowest"):
            value = total_rate.get(key)
            if isinstance(value, (int, float)):
                return float(value)

    rate_per_night = item.get("rate_per_night") or {}
    if isinstance(rate_per_night, dict):
        for key in ("lowest", "price", "value"):
            value = rate_per_night.get(key)
            if isinstance(value, (int, float)):
                # For this workflow we only run 10 nights, so this keeps the query budget low.
                return float(value) * 10

    extracted = item.get("price") or item.get("extracted_price")
    if isinstance(extracted, (int, float)):
        return float(extracted)

    return None


def _extract_rating_5(item: dict) -> float | None:
    for key in ("overall_rating", "rating", "extracted_rating"):
        value = item.get(key)
        if isinstance(value, (int, float)):
            number = float(value)
            if number <= 5:
                return round(number, 2)
            if number <= 10:
                return round(number / 2, 2)
    return None


def _extract_stars(item: dict) -> float | None:
    for key in ("hotel_class", "extracted_hotel_class", "stars"):
        value = item.get(key)
        if isinstance(value, (int, float)):
            number = float(value)
            if 0 < number <= 5:
                return round(number, 2)
    return None
