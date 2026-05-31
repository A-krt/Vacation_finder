from __future__ import annotations

from app.adapters.transfers_base import BaseTransferAdapter
from app.models import AccommodationOption, TransferOption


TRANSFER_PRICE = {
    "ALC": 32.0,
    "AGP": 36.0,
    "VLC": 30.0,
    "PMI": 38.0,
    "FAO": 34.0,
    "LIS": 28.0,
    "NAP": 30.0,
    "CTA": 34.0,
    "BRI": 26.0,
    "NCE": 34.0,
    "SPU": 36.0,
    "DBV": 46.0,
    "HER": 38.0,
    "CHQ": 42.0,
    "RHO": 40.0,
    "MLA": 24.0,
    "LCA": 36.0,
    "PFO": 38.0,
}


class MockTransferAdapter(BaseTransferAdapter):
    def get_transfer_cost(
        self,
        arrival_airport: str,
        accommodation: AccommodationOption,
    ) -> TransferOption:
        total = TRANSFER_PRICE.get(arrival_airport, 35.0)
        half = round(total / 2, 2)

        return TransferOption(
            arrival_airport=arrival_airport,
            estimated=True,
            arrival_transfer_cost=half,
            departure_transfer_cost=round(total - half, 2),
            total_price=round(total, 2),
            source="mock_transfers",
        )
