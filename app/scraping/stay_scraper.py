from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional
from urllib.parse import urlencode

from playwright.sync_api import BrowserContext, Locator, Page

from app.scraping.booking_url_builder import build_booking_search_url
from app.scraping.expedia_url_builder import build_expedia_search_url
from app.scraping.parsers import (
    parse_hotel_stars,
    parse_price_to_float,
    parse_review_score,
)
from app.scraping.selectors import StaySiteConfig


@dataclass(frozen=True)
class RawStayResult:
    property_name: str
    property_type: str | None
    total_price: float | None
    review_score_5: float | None
    review_score_10: float | None
    hotel_stars: float | None
    private_bathroom: bool
    bed_type: str
    url: str | None
    raw_review_text: str | None = None
    raw_stars_text: str | None = None
    raw_price_text: str | None = None


class StayScraper:
    def __init__(self, site_config: StaySiteConfig) -> None:
        self.site_config = site_config

    def build_search_url(
        self,
        destination_query: str,
        checkin: date,
        checkout: date,
        adults: int,
    ) -> str:
        builder = self.site_config.search_url_builder_name

        if builder == "template":
            params = {
                "destination": destination_query,
                "checkin": checkin.isoformat(),
                "checkout": checkout.isoformat(),
                "adults": adults,
            }
            return f"{self.site_config.base_url}?{urlencode(params)}"

        if builder == "booking_search_results":
            return build_booking_search_url(
                destination_query=destination_query,
                checkin=checkin,
                checkout=checkout,
                adults=adults,
            )

        if builder == "expedia_search_results":
            return build_expedia_search_url(
                destination_query=destination_query,
                checkin=checkin,
                checkout=checkout,
                adults=adults,
            )

        raise ValueError(f"Unknown search URL builder: {builder}")

    def scrape(
        self,
        context: BrowserContext,
        destination_query: str,
        checkin: date,
        checkout: date,
        adults: int,
        max_results: int = 20,
    ) -> list[RawStayResult]:
        page = context.new_page()

        search_url = self.build_search_url(
            destination_query=destination_query,
            checkin=checkin,
            checkout=checkout,
            adults=adults,
        )

        page.goto(search_url, wait_until="domcontentloaded")
        self._handle_cookie_banner(page)
        self._maybe_load_more(page)

        results = self._parse_result_cards(page, max_results=max_results)
        page.close()
        return results

    def _handle_cookie_banner(self, page: Page) -> None:
        if not self.site_config.cookie_accept_button:
            return

        locator = page.locator(self.site_config.cookie_accept_button)

        try:
            if locator.count() > 0:
                locator.first.click(timeout=4_000)
        except Exception:
            pass

    def _maybe_load_more(self, page: Page) -> None:
        if not self.site_config.load_more_button:
            return

        locator = page.locator(self.site_config.load_more_button)

        try:
            if locator.count() > 0:
                locator.first.click(timeout=5_000)
        except Exception:
            pass

    def _parse_result_cards(self, page: Page, max_results: int = 20) -> list[RawStayResult]:
        locator = page.locator(self.site_config.result_card)

        try:
            locator.first.wait_for(timeout=20_000)
        except Exception:
            return []

        cards = locator
        count = min(cards.count(), max_results)

        results: list[RawStayResult] = []
        for idx in range(count):
            card = cards.nth(idx)
            results.append(self._parse_card(card))

        return results

    def _parse_card(self, card: Locator) -> RawStayResult:
        property_name = self._safe_inner_text(card, self.site_config.property_name) or "Unknown property"

        property_type = (
            self._safe_inner_text(card, self.site_config.property_type)
            if self.site_config.property_type
            else None
        )

        raw_price_text = self._safe_inner_text(card, self.site_config.total_price)
        total_price = parse_price_to_float(raw_price_text)

        raw_review_text = (
            self._safe_inner_text(card, self.site_config.review_text)
            if self.site_config.review_text
            else None
        )
        review_score_5, review_score_10 = parse_review_score(raw_review_text)

        raw_stars_text = (
            self._safe_inner_text(card, self.site_config.stars_text)
            if self.site_config.stars_text
            else None
        )
        hotel_stars = parse_hotel_stars(raw_stars_text)

        private_bathroom = self._text_contains(
            card,
            self.site_config.private_bathroom_text,
            ["private bathroom", "eigen badkamer"],
        )

        bed_type = (
            "double"
            if self._text_contains(
                card,
                self.site_config.bed_text,
                ["double", "tweepersoonsbed", "double bed", "queen bed", "king bed"],
            )
            else "unknown"
        )

        url = (
            self._safe_attribute(card, self.site_config.property_link, "href")
            if self.site_config.property_link
            else None
        )

        return RawStayResult(
            property_name=property_name,
            property_type=property_type,
            total_price=total_price,
            review_score_5=review_score_5,
            review_score_10=review_score_10,
            hotel_stars=hotel_stars,
            private_bathroom=private_bathroom,
            bed_type=bed_type,
            url=url,
            raw_review_text=raw_review_text,
            raw_stars_text=raw_stars_text,
            raw_price_text=raw_price_text,
        )

    def _safe_inner_text(self, root: Locator, selector: str | None) -> Optional[str]:
        if not selector:
            return None

        locator = root.locator(selector)

        try:
            if locator.count() == 0:
                return None
            return locator.first.inner_text(timeout=3_000).strip()
        except Exception:
            return None

    def _safe_attribute(
        self,
        root: Locator,
        selector: str | None,
        attribute: str,
    ) -> Optional[str]:
        if not selector:
            return None

        locator = root.locator(selector)

        try:
            if locator.count() == 0:
                return None
            return locator.first.get_attribute(attribute, timeout=3_000)
        except Exception:
            return None

    def _text_contains(self, root: Locator, selector: str | None, needles: list[str]) -> bool:
        text = self._safe_inner_text(root, selector)
        if not text:
            return False

        lowered = text.lower()
        return any(needle.lower() in lowered for needle in needles)
