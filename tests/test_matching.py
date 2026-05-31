from app.adapters.flights_mock import MockFlightAdapter
from app.adapters.stays_mock import MockStayAdapter
from app.adapters.transfers_mock import MockTransferAdapter
from app.config import get_settings
from app.destinations.seed_list import DESTINATIONS
from app.generators.date_generator import generate_trip_date_options
from app.services.matching_service import build_trip_results


SETTINGS = get_settings()


def test_build_trip_results_returns_budget_valid_results() -> None:
    destination = DESTINATIONS[0]
    date_option = generate_trip_date_options(((2026, 7),), (9,))[0]

    stays = MockStayAdapter().search_stays(
        destination.arrival_airport,
        date_option.departure_date,
        date_option.return_date,
        2,
    )

    results = build_trip_results(
        destination=destination,
        date_option=date_option,
        stays=stays,
        flight_adapter=MockFlightAdapter(),
        transfer_adapter=MockTransferAdapter(),
        settings=SETTINGS,
    )

    assert all(r.trip_total <= SETTINGS.total_budget for r in results)
