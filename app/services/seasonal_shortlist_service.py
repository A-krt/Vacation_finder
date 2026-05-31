from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.models import TripResult
from app.services.verification_links import (
    create_shortlist_rows,
    create_verification_rows,
    export_shortlist_to_csv,
    export_verification_links_to_csv,
)
from app.utils.time_utils import timestamp_for_filename


def export_seasonal_shortlist_artifacts(results: list[TripResult]) -> dict[str, str]:
    settings = get_settings()
    timestamp = timestamp_for_filename(settings.timezone_name)

    shortlist_rows = create_shortlist_rows(results, settings.top_shortlist_n)
    verification_rows = create_verification_rows(results, settings.top_shortlist_n)

    shortlist_path = settings.shortlist_dir / f"{settings.csv_prefix}_shortlist_{timestamp}.csv"
    verification_path = settings.verification_dir / f"{settings.csv_prefix}_verification_links_{timestamp}.csv"

    exported_shortlist = export_shortlist_to_csv(shortlist_rows, shortlist_path)
    exported_verification = export_verification_links_to_csv(verification_rows, verification_path)

    return {
        "shortlist_csv": exported_shortlist,
        "verification_links_csv": exported_verification,
    }
