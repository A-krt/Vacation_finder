from app.generators.date_generator import generate_trip_date_options


def test_generate_trip_date_options_count() -> None:
    options = generate_trip_date_options(((2026, 7),), (9, 10, 11))
    assert len(options) == 31 * 3
    assert options[0].nights == 9
