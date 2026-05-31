from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return int(value)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return float(value)


def _env_csv_tuple(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _env_int_tuple(name: str, default: tuple[int, ...]) -> tuple[int, ...]:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return tuple(int(item.strip()) for item in value.split(",") if item.strip())


def _env_months_tuple(
    name: str,
    default: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default

    results: list[tuple[int, int]] = []
    for raw in value.split(","):
        raw = raw.strip()
        if not raw:
            continue
        year_str, month_str = raw.split("-")
        results.append((int(year_str), int(month_str)))
    return tuple(results)


@dataclass(frozen=True)
class Settings:
    departure_airport: str = os.getenv("DEPARTURE_AIRPORT", "AMS")
    adults: int = _env_int("ADULTS", 2)
    total_budget: float = _env_float("TOTAL_BUDGET", 1500.0)
    budget_per_person: float = field(init=False)

    allowed_departure_months: Tuple[tuple[int, int], ...] = _env_months_tuple(
        "ALLOWED_MONTHS",
        ((2026, 8),),
    )
    nights_options: Tuple[int, ...] = _env_int_tuple("NIGHTS_OPTIONS", (10,))

    direct_flights_only: bool = True
    checked_bags_total: int = 1
    checked_bag_fee_estimate_total: float = _env_float("CHECKED_BAG_FEE_ESTIMATE_TOTAL", 70.0)

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
    top_shortlist_n: int = _env_int("TOP_SHORTLIST_N", 20)

    timezone_name: str = "Europe/Amsterdam"

    output_dir: Path = Path("output/results")
    shortlist_dir: Path = Path("output/shortlists")
    verification_dir: Path = Path("output/verification")
    audit_dir: Path = Path("output/audit")
    screenshot_dir: Path = Path("output/screenshots")
    logs_dir: Path = Path("logs")

    csv_prefix: str = os.getenv("OUTPUT_LABEL", "august_live_results")

    destination_filters: tuple[str, ...] = _env_csv_tuple(
        "DESTINATION_FILTERS",
        ("Antalya", "Benidorm", "Valencia"),
    )

    # Default OFF so tests/workflows without a key still run safely.
    use_live_stay_scrapers: bool = _env_bool("USE_LIVE_STAY_SCRAPERS", False)
    use_live_flight_sources: bool = _env_bool("USE_LIVE_FLIGHT_SOURCES", False)

    stay_provider_order: tuple[str, ...] = ("serpapi", "mock")
    flight_provider_order: tuple[str, ...] = ("serpapi", "mock")

    provider_max_results: int = 10

    serpapi_api_key: str | None = os.getenv("SERPAPI_API_KEY")
    serpapi_timeout_seconds: int = _env_int("SERPAPI_TIMEOUT_SECONDS", 40)
    serpapi_currency: str = os.getenv("SERPAPI_CURRENCY", "EUR")
    serpapi_language: str = os.getenv("SERPAPI_LANGUAGE", "en")
    serpapi_country: str = os.getenv("SERPAPI_COUNTRY", "nl")

    def __post_init__(self) -> None:
        object.__setattr__(self, "budget_per_person", round(self.total_budget / max(self.adults, 1), 2))


_SETTINGS = Settings()


def get_settings() -> Settings:
    return _SETTINGS
