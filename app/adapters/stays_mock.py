from __future__ import annotations

from datetime import date
import hashlib

from app.adapters.stays_base import BaseStayAdapter
from app.models import AccommodationOption


PROPERTY_TYPES = ["hotel", "apartment", "holiday_home"]
NAME_PREFIXES = ["Sun", "Blue", "Coastal", "Harbor", "Marina", "Vista"]
NAME_SUFFIXES = ["Suites", "Residences", "Apartments", "House", "Hotel", "Retreat"]

DESTINATION_NIGHTLY = {
    "ALC": 78,
    "AGP": 85,
    "VLC": 82,
    "PMI": 95,
    "FAO": 74,
    "LIS": 88,
    "NAP": 86,
    "CTA": 92,
    "BRI": 80,
    "NCE": 102,
    "SPU": 96,
    "DBV": 106,
    "HER": 90,
    "CHQ": 94,
    "RHO": 98,
    "MLA": 91,
    "LCA": 104,
    "PFO": 100,
}


class MockStayAdapter(BaseStayAdapter):
    def _seed(self, *parts: str) -> int:
        digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
        return int(digest[:8], 16)

    def search_stays(
        self,
        destination_code: str,
        checkin: date,
        checkout: date,
        adults: int,
    ) -> list[AccommodationOption]:
        nights = (checkout - checkin).days
        seed = self._seed(destination_code, str(checkin), str(checkout), str(adults))
        base_nightly = DESTINATION_NIGHTLY.get(destination_code, 90)
        season_factor = ((checkin.day % 7) * 2) + ((checkout.day % 5) * 3)
        results: list[AccommodationOption] = []

        for idx in range(5):
            property_type = PROPERTY_TYPES[(seed + idx) % len(PROPERTY_TYPES)]
            stars = 4.0 + (((seed + idx) % 3) * 0.5) if property_type == "hotel" else None
            review_5 = None if idx == 1 else round(4.0 + (((seed + idx) % 8) / 20), 1)
            review_10 = None if idx == 2 else round(8.0 + (((seed + idx) % 16) / 10), 1)
            nightly = base_nightly + season_factor + (idx * 8) + ((seed % 13) - 6)
            total_price = max(320.0, round(nightly * nights + 20 + idx * 15, 2))
            booking_fee = round(12.0 + idx * 3.5, 2)
            name = f"{NAME_PREFIXES[(seed + idx) % len(NAME_PREFIXES)]} {NAME_SUFFIXES[(seed // 3 + idx) % len(NAME_SUFFIXES)]}"

            results.append(
                AccommodationOption(
                    property_name=name,
                    destination_code=destination_code,
                    property_type=property_type,
                    checkin=checkin,
                    checkout=checkout,
                    nights=nights,
                    adults=adults,
                    total_price=total_price,
                    booking_fee=booking_fee,
                    private_bathroom=True,
                    bed_type="double",
                    hotel_stars=stars,
                    review_score_5=review_5,
                    review_score_10=review_10,
                    latitude=None,
                    longitude=None,
                    source="mock_stays",
                    url=f"https://example.com/stays/{destination_code}/{idx}",
                )
            )

        return sorted(results, key=lambda s: s.total_price)
