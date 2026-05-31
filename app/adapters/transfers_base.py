from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import AccommodationOption, TransferOption


class BaseTransferAdapter(ABC):
    @abstractmethod
    def get_transfer_cost(
        self,
        arrival_airport: str,
        accommodation: AccommodationOption,
    ) -> TransferOption:
        raise NotImplementedError
