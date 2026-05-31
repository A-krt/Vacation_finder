from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from app.adapters.stays_base import BaseStayAdapter
from app.adapters.stays_mock import MockStayAdapter
from app.config import Settings, get_settings
from app.live_data.models import ProviderAttempt, SearchAudit
from app.live_data.utils import dedupe_by_lowest_price, normalize_property_name
from app.models import AccommodationOption
from app.utils.logger import get_logger


logger = get_logger(__name__)


class HybridStayAdapter(BaseStayAdapter):
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.last_audit: Optional[SearchAudit] = None

    def search_stays(
        self,
        destination_code: str,
        checkin: date,
        checkout: date,
        adults: int,
    ) -> list[AccommodationOption]:
        audit = SearchAudit(search_timestamp=datetime.utcnow(), category="stays")
        providers = self._build_providers()
        all_results: list[AccommodationOption] = []

        for provider_name, provider in providers:
            try:
                results = provider.search_stays(destination_code, checkin, checkout, adults)

                audit.add_attempt(
                    ProviderAttempt(
                        provider_name=provider_name,
                        success=True,
                        blocked=False,
                        results_count=len(results),
                    )
                )

                if results:
                    all_results.extend(results)
                    logger.info("Stay provider %s gaf %s resultaten terug", provider_name, len(results))
                else:
                    logger.info("Stay provider %s gaf 0 resultaten terug", provider_name)

            except Exception as exc:
                blocked = any(
                    token in str(exc).lower()
                    for token in ["bot", "captcha", "blocked", "challenge", "human side", "datadome"]
                )

                audit.add_attempt(
                    ProviderAttempt(
                        provider_name=provider_name,
                        success=False,
                        blocked=blocked,
                        results_count=0,
                        error_message=str(exc),
                    )
                )
                logger.warning("Stay provider %s faalde: %s", provider_name, exc)

        if not all_results:
            logger.warning("Geen stay-resultaten via live providers; fallback naar mock-data.")
            mock_results = MockStayAdapter().search_stays(destination_code, checkin, checkout, adults)

            audit.add_attempt(
                ProviderAttempt(
                    provider_name="mock-fallback",
                    success=True,
                    blocked=False,
                    results_count=len(mock_results),
                    notes="Automatische fallback omdat live providers geen resultaten gaven.",
                )
            )
            all_results.extend(mock_results)

        deduped = dedupe_by_lowest_price(
            all_results,
            key_getter=lambda item: normalize_property_name(item.property_name),
            price_getter=lambda item: item.total_price + item.booking_fee,
        )
        deduped.sort(key=lambda x: x.total_price + x.booking_fee)

        self.last_audit = audit
        return deduped

    def _build_providers(self):
        providers = []

        if self.settings.use_live_stay_scrapers:
            for name in self.settings.stay_provider_order:
                provider = self._create_named_provider(name)
                if provider is not None:
                    providers.append((name, provider))
        else:
            providers.append(("mock", MockStayAdapter()))

        return providers

    def _create_named_provider(self, name: str):
        lowered = name.lower()

        if lowered == "mock":
            return MockStayAdapter()

        if lowered == "booking":
            from app.adapters.stays_booking import BookingStayAdapter
            return BookingStayAdapter(
                headless=True,
                max_results=self.settings.provider_max_results,
            )

        if lowered == "expedia":
            from app.adapters.stays_expedia import ExpediaStayAdapter
            return ExpediaStayAdapter(
                headless=True,
                max_results=self.settings.provider_max_results,
            )

        return None
