from __future__ import annotations

from app.adapters.flights_hybrid import HybridFlightAdapter
from app.adapters.stays_hybrid import HybridStayAdapter
from app.adapters.transfers_mock import MockTransferAdapter
from app.config import Settings, get_settings
from app.live_data.audit import write_audit_file
from app.utils.time_utils import timestamp_for_filename


def build_default_hybrid_adapters(settings: Settings | None = None):
    settings = settings or get_settings()
    flight_adapter = HybridFlightAdapter(settings)
    stay_adapter = HybridStayAdapter(settings)
    transfer_adapter = MockTransferAdapter()
    return flight_adapter, stay_adapter, transfer_adapter


def write_provider_audits(
    flight_adapter: HybridFlightAdapter,
    stay_adapter: HybridStayAdapter,
    settings: Settings | None = None,
) -> list[str]:
    settings = settings or get_settings()
    ts = timestamp_for_filename(settings.timezone_name)
    written: list[str] = []

    if stay_adapter.last_audit is not None:
        stay_path = settings.audit_dir / f"stay_provider_audit_{ts}.json"
        write_audit_file(stay_adapter.last_audit, stay_path)
        written.append(str(stay_path))

    if flight_adapter.last_audit is not None:
        flight_path = settings.audit_dir / f"flight_provider_audit_{ts}.json"
        write_audit_file(flight_adapter.last_audit, flight_path)
        written.append(str(flight_path))

    return written
