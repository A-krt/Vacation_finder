from __future__ import annotations

from calendar import monthrange
from datetime import date, timedelta

from app.models import TripDateOption


def generate_trip_date_options(
    allowed_months: list[tuple[int, int]] | tuple[tuple[int, int], ...],
    nights_options: list[int] | tuple[int, ...],
) -> list[TripDateOption]:
    results: list[TripDateOption] = []
    for year, month in allowed_months:
        days_in_month = monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            departure = date(year, month, day)
            for nights in nights_options:
                results.append(
                    TripDateOption(
                        departure_date=departure,
                        return_date=departure + timedelta(days=nights),
                        nights=nights,
                    )
                )
    return results
