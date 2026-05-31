from __future__ import annotations

from datetime import date
from urllib.parse import urlencode


def build_booking_search_url(destination_query: str, checkin: date, checkout: date, adults: int) -> str:
    params = {
        "ss": destination_query,
        "checkin": checkin.isoformat(),
        "checkout": checkout.isoformat(),
        "group_adults": adults,
        "no_rooms": 1,
        "group_children": 0,
        "selected_currency": "EUR",
    }
    return f"https://www.booking.com/searchresults.html?{urlencode(params)}"
