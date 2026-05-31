from __future__ import annotations

from datetime import date
import hashlib

from app.adapters.flights_base import BaseFlightAdapter
from app.models import FlightOption


DESTINATION_BASE_PRICE = {
    "ALC": 280,
    "AGP": 300,
    "VLC": 290,
    "PMI": 320,
    "FAO": 260,
    "LIS": 310,
    "NAP": 300,
    "CTA": 340,
    "BRI": 320,
    "NCE": 330,
    "SPU": 350,
    "DBV": 380,
    "HER": 360,
    "CHQ": 370,
    "RHO": 390,
    "MLA": 330,
    "LCA": 420,
    "PFO": 410,
}

AIRLINES = ["KLM", "Transavia", "easyJet", "Vueling", "Ryanair"]


class MockFlightAdapter(BaseFlightAdapter):
    def _seed(self, *parts: str) -> int:
        digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
        return int(digest[:8], 16)

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
        seed = self._seed(origin, destination, str(departure_date), str(return_date), str(adults))
        base = DESTINATION_BASE_PRICE.get(destination, 340)
        day_factor = ((departure_date.day + return_date.day) % 9) * 8
        duration_factor = (return_date - departure_date).days * 5
        options: list[FlightOption] = []

        for idx in range(3):
            fluctuation = (seed % (31 + idx * 5)) - 10 + idx * 20
            airline = AIRLINES[(seed + idx) % len(AIRLINES)]
            base_price = max(140.0, float(base + day_factor + duration_factor + fluctuation))
            bag_fee = 55.0 if checked_bags_total >= 1 else 0.0
            booking_fee = 14.0 + (idx * 3)
            total_price = round(base_price + bag_fee + booking_fee, 2)

            options.append(
                FlightOption(
                    origin=origin,
                    destination=destination,
                    departure_date=departure_date,
                    return_date=return_date,
                    airline=airline,
                    is_direct=True,
                    adults=adults,
                    base_price=round(base_price, 2),
                    bag_fee=bag_fee,
                    booking_fee=booking_fee,
                    total_price=total_price,
                    checked_bag_included=checked_bags_total >= 1,
                    source="mock_flights",
                    url=f"https://example.com/flights/{origin}/{destination}",
                )
            )

        return sorted(options, key=lambda f: f.total_price)
