from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from app.adapters.flights_base import BaseFlightAdapter
from app.adapters.flights_mock import MockFlightAdapter
from app.adapters.flights_serpapi import SerpApiFlightAdapter
from app.config import Settings, get_settings
from app.live_data.models import ProviderAttempt, SearchAudit
from app.models import FlightOption
from app.utils.logger import get_logger


logger = get_logger(__name__)


class HybridFlightAdapter(BaseFlightAdapter):
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.last_audit: Optional[SearchAudit] = None
        self._cache: dict[tuple, list[FlightOption]] = {}

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
        key = (
            origin,
            destination,
            departure_date.isoformat(),
            return_date.isoformat(),
            adults,
            direct_only,
            checked_bags_total,
        )

        if key in self._cache:
            return self._cache[key]

        audit = self.last_audit or SearchAudit(
            search_timestamp=datetime.utcnow(),
            category="flights",
        )
        providers = self._build_providers()

        for provider_name, provider in providers:
            try:
                results = provider.search_flights(
                    origin=origin,
                    destination=destination,
                    departure_date=departure_date,
                    return_date=return_date,
                    adults=adults,
                    direct_only=direct_only,
                    checked_bags_total=checked_bags_total,
                )

                audit.add_attempt(
                    ProviderAttempt(
                        provider_name=provider_name,
                        success=True,
                        blocked=False,
                        results_count=len(results),
                    )
                )

                if results:
                    self.last_audit = audit
                    self._cache[key] = results
                    return results

            except Exception as exc:
                audit.add_attempt(
                    ProviderAttempt(
                        provider_name=provider_name,
                        success=False,
                        blocked=False,
                        results_count=0,
                        error_message=str(exc),
                    )
                )
                logger.warning("Flight provider %s faalde: %s", provider_name, exc)

        mock_results = MockFlightAdapter().search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            adults=adults,
            direct_only=direct_only,
            checked_bags_total=checked_bags_total,
        )

        audit.add_attempt(
            ProviderAttempt(
                provider_name="mock-fallback",
                success=True,
                blocked=False,
                results_count=len(mock_results),
                notes="Fallback omdat live flight provider geen resultaten gaf.",
            )
        )

        self.last_audit = audit
        self._cache[key] = mock_results
        return mock_results

    def _build_providers(self):
        providers = []

        if self.settings.use_live_flight_sources:
            for name in self.settings.flight_provider_order:
                if name == "serpapi":
                    providers.append((name, SerpApiFlightAdapter(self.settings)))
                elif name == "mock":
                    providers.append((name, MockFlightAdapter()))
        else:
            providers.append(("mock", MockFlightAdapter()))

        return providers
