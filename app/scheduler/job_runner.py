from __future__ import annotations

from pathlib import Path

from app.adapters.flights_mock import MockFlightAdapter
from app.adapters.stays_mock import MockStayAdapter
from app.adapters.transfers_mock import MockTransferAdapter
from app.config import get_settings
from app.services.export_service import export_results_to_csv, print_top_results
from app.services.search_service import run_search
from app.utils.logger import get_logger
from app.utils.time_utils import timestamp_for_filename


logger = get_logger(__name__)


def run_daily_job() -> Path:
    settings = get_settings()
    logger.info("Dagelijkse job gestart")

    flight_adapter = MockFlightAdapter()
    stay_adapter = MockStayAdapter()
    transfer_adapter = MockTransferAdapter()

    results = run_search(
        flight_adapter=flight_adapter,
        stay_adapter=stay_adapter,
        transfer_adapter=transfer_adapter,
    )

    print_top_results(results, top_n=settings.top_results_terminal)

    timestamp = timestamp_for_filename(settings.timezone_name)
    output_path = settings.output_dir / f"{settings.csv_prefix}_{timestamp}.csv"
    export_results_to_csv(results, output_path)

    logger.info("Dagelijkse job afgerond. CSV opgeslagen op %s", output_path)
    return output_path
