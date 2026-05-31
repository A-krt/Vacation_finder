from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from app.models import FlightOption


class BaseFlightAdapter(ABC):
    @abstractmethod
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
        raise NotImplementedError
