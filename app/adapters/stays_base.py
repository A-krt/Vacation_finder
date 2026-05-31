from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from app.models import AccommodationOption


class BaseStayAdapter(ABC):
    @abstractmethod
    def search_stays(
        self,
        destination_code: str,
        checkin: date,
        checkout: date,
        adults: int,
    ) -> list[AccommodationOption]:
        raise NotImplementedError
