from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class Settings:
    departure_airport: str = "AMS"
    adults: int = 2
    total_budget: float = 1500.0
    budget_per_person: float = 750.0
    allowed_departure_months: Tuple[tuple[int, int], ...] = ((2026, 7), (2026, 8))
    nights_options: Tuple[int, ...] = (9, 10, 11)
    direct_flights_only: bool = True
    checked_bags_total: int = 1
    allowed_accommodation_types: tuple[str, ...] = ("hotel", "apartment", "holiday_home")
    require_private_bathroom: bool = True
    require_bed_type: str = "double"
    min_hotel_stars: float = 4.0
    min_review_5: float = 4.0
    min_review_10: float = 8.0
    include_transfers: bool = True
    include_booking_fees: bool = True
    ranking_weights: dict[str, float] = field(
        default_factory=lambda: {
            "price": 0.40,
            "quality": 0.35,
            "destination_fit": 0.25,
        }
    )
    top_results_terminal: int = 10
    timezone_name: str = "Europe/Amsterdam"
    output_dir: Path = Path("output/results")
    screenshot_dir: Path = Path("output/screenshots")
    logs_dir: Path = Path("logs")
    csv_prefix: str = "vacation_results"


_SETTINGS = Settings()


def get_settings() -> Settings:
    return _SETTINGS
