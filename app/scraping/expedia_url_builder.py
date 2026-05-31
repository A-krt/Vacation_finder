from __future__ import annotations

from datetime import date
from urllib.parse import urlencode


# Eerste werkhypothese voor Expedia stay search URL.
# Deze valideren we met expedia_probe.py artifacts.
def build_expedia_search_url(destination_query: str, checkin: date, checkout: date, adults: int) -> str:
    params = {
        "destination": destination_query,
        "startDate": checkin.isoformat(),
        "endDate": checkout.isoformat(),
        "rooms": 1,
        "adults": adults,
    }
    return f"https://www.expedia.com/Hotel-Search?{urlencode(params)}"
