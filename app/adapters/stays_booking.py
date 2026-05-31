from __future__ import annotations

from datetime import date

from app.adapters.stays_base import BaseStayAdapter
from app.destinations.seed_list import DESTINATIONS
from app.models import AccommodationOption
from app.scraping.browser_manager import BrowserConfig, BrowserManager
from app.scraping.selectors_booking import BOOKING_STAY_SITE_CONFIG
from app.scraping.stay_scraper import RawStayResult, StayScraper


_DESTINATION_LOOKUP = {d.arrival_airport: d.city for d in DESTINATIONS}


class BookingStayAdapter(BaseStayAdapter):
    def __init__(self, headless: bool = True, max_results: int = 20) -> None:
        self.browser_config = BrowserConfig(headless=headless)
        self.max_results = max_results
        self.site_config = BOOKING_STAY_SITE_CONFIG

    def search_stays(
        self,
        destination_code: str,
        checkin: date,
        checkout: date,
        adults: int,
    ) -> list[AccommodationOption]:
        destination_query = _DESTINATION_LOOKUP.get(destination_code, destination_code)
        scraper = StayScraper(self.site_config)

        with BrowserManager(self.browser_config) as manager:
            context = manager.new_context()
            raw_results = scraper.scrape(
                context=context,
                destination_query=destination_query,
                checkin=checkin,
                checkout=checkout,
                adults=adults,
                max_results=self.max_results,
            )
            context.close()

        return [
            self._to_accommodation_option(r, destination_code, checkin, checkout, adults)
            for r in raw_results
            if r.total_price is not None
        ]

    def _to_accommodation_option(
        self,
        raw: RawStayResult,
        destination_code: str,
        checkin: date,
        checkout: date,
        adults: int,
    ) -> AccommodationOption:
        nights = (checkout - checkin).days

        property_type = (raw.property_type or "hotel").strip().lower().replace(" ", "_")
        if property_type not in {"hotel", "apartment", "holiday_home"}:
            property_type = "hotel"

        return AccommodationOption(
            property_name=raw.property_name,
            destination_code=destination_code,
            property_type=property_type,
            checkin=checkin,
            checkout=checkout,
            nights=nights,
            adults=adults,
            total_price=raw.total_price or 0.0,
            booking_fee=0.0,
            private_bathroom=raw.private_bathroom,
            bed_type="double" if raw.bed_type == "double" else "unknown",
            hotel_stars=raw.hotel_stars,
            review_score_5=raw.review_score_5,
            review_score_10=raw.review_score_10,
            source="playwright:booking.com",
            url=raw.url,
        )
