from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from app.adapters.flights_base import BaseFlightAdapter
from app.adapters.flights_mock import MockFlightAdapter
from app.config import Settings, get_settings
from app.live_data.models import ProviderAttempt, SearchAudit
from app.models import FlightOption
from app.utils.logger import get_logger


logger = get_logger(__name__)


class HybridFlightAdapter(BaseFlightAdapter):
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.last_audit: Optional[SearchAudit] = None

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
        audit = SearchAudit(search_timestamp=datetime.utcnow(), category="flights")

        results = MockFlightAdapter().search_flights(
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
                provider_name="mock",
                success=True,
                blocked=False,
                results_count=len(results),
                notes="Flights blijven voorlopig mock totdat een stabiele live bron is gekozen.",
            )
        )

        self.last_audit = audit
        logger.info("Flight provider mock gaf %s resultaten terug", len(results))
        return results
