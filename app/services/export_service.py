from __future__ import annotations

from pathlib import Path

from app.models import TripResult
from app.utils.csv_utils import write_csv_rows
from app.utils.money_utils import fmt_eur


def print_top_results(results: list[TripResult], top_n: int = 10) -> None:
    if not results:
        print("Geen geldige reizen gevonden.")
        return

    for result in results[:top_n]:
        text = (
            f"#{result.rank} {result.destination_city}, {result.destination_country} | "
            f"{result.departure_date} -> {result.return_date} | {result.nights} nachten\n"
            f"  Vlucht: {fmt_eur(result.flight.total_price)} | "
            f"Verblijf: {fmt_eur(result.accommodation.total_price + result.accommodation.booking_fee)} | "
            f"Transfers: {fmt_eur(result.transfer.total_price)}\n"
            f"  Totaal: {fmt_eur(result.trip_total)} ({fmt_eur(result.trip_total_per_person)} p.p.)\n"
            f"  Verblijf: {result.accommodation.property_name} ({result.accommodation.property_type})\n"
            f"  Kwaliteit: {result.accommodation_quality_score:.2f}/10 | "
            f"Bestemming-fit: {result.destination_fit_score:.2f}/10 | "
            f"Value score: {result.value_score:.4f}\n"
        )
        print(text)


def export_results_to_csv(results: list[TripResult], output_path: Path | str) -> str:
    output_path = Path(output_path)
    rows = []

    for result in results:
        rows.append(
            {
                "search_timestamp": result.search_timestamp.isoformat(),
                "rank": result.rank,
                "destination": result.destination_city,
                "destination_country": result.destination_country,
                "departure_airport": result.flight.origin,
                "arrival_airport": result.arrival_airport,
                "departure_date": result.departure_date.isoformat(),
                "return_date": result.return_date.isoformat(),
                "nights": result.nights,
                "adults": result.flight.adults,
                "property_name": result.accommodation.property_name,
                "property_type": result.accommodation.property_type,
                "private_bathroom": result.accommodation.private_bathroom,
                "bed_type": result.accommodation.bed_type,
                "hotel_stars": result.accommodation.hotel_stars,
                "review_score_5": result.accommodation.review_score_5,
                "review_score_10": result.accommodation.review_score_10,
                "accommodation_quality_score": result.accommodation_quality_score,
                "destination_fit_score": result.destination_fit_score,
                "flight_total": result.flight.total_price,
                "stay_total": round(result.accommodation.total_price + result.accommodation.booking_fee, 2),
                "transfer_total": result.transfer.total_price,
                "booking_fees_total": round(result.flight.booking_fee + result.accommodation.booking_fee, 2),
                "trip_total": result.trip_total,
                "trip_total_per_person": result.trip_total_per_person,
                "price_score": result.price_score,
                "value_score": result.value_score,
                "flight_carrier": result.flight.airline,
                "is_direct": result.flight.is_direct,
                "checked_bag_included": result.flight.checked_bag_included,
                "transfer_estimated": result.transfer.estimated,
                "source_flight": result.flight.source,
                "source_stay": result.accommodation.source,
                "notes": "mock-data run",
            }
        )

    return write_csv_rows(rows, output_path)
