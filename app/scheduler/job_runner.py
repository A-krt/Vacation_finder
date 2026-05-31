from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.services.export_service import export_results_to_csv, print_top_results
from app.services.hybrid_strategy_service import (
    build_default_hybrid_adapters,
    write_provider_audits,
)
from app.services.search_service import run_search
from app.services.seasonal_shortlist_service import export_seasonal_shortlist_artifacts
from app.utils.logger import get_logger
from app.utils.time_utils import timestamp_for_filename


logger = get_logger(__name__)


def run_daily_job() -> Path:
    settings = get_settings()
    logger.info("Seasonal shortlist job gestart")

    flight_adapter, stay_adapter, transfer_adapter = build_default_hybrid_adapters(settings)

    results = run_search(
        flight_adapter=flight_adapter,
        stay_adapter=stay_adapter,
        transfer_adapter=transfer_adapter,
    )
    print_top_results(results, top_n=settings.top_results_terminal)

    timestamp = timestamp_for_filename(settings.timezone_name)
    output_path = settings.output_dir / f"{settings.csv_prefix}_{timestamp}.csv"
    export_results_to_csv(results, output_path)

    shortlist_exports = export_seasonal_shortlist_artifacts(results)
    audit_files = write_provider_audits(flight_adapter, stay_adapter, settings)

    logger.info("Volledige resultaten CSV opgeslagen op %s", output_path)
    logger.info("Shortlist CSV opgeslagen op %s", shortlist_exports["shortlist_csv"])
    logger.info(
        "Verification links CSV opgeslagen op %s",
        shortlist_exports["verification_links_csv"],
    )

    if audit_files:
        logger.info("Provider audit bestanden geschreven: %s", ", ".join(audit_files))

    logger.info("Seasonal shortlist job afgerond")
    return output_path
