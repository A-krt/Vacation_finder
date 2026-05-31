from __future__ import annotations

from datetime import date

from app.adapters.stays_playwright import PlaywrightStayAdapter
from app.scraping.selectors import DEFAULT_STAY_SITE_CONFIG


if __name__ == "__main__":
    adapter = PlaywrightStayAdapter(
        site_config=DEFAULT_STAY_SITE_CONFIG,
        headless=True,
        max_results=5,
    )

    results = adapter.search_stays(
        destination_code="ALC",
        checkin=date(2026, 7, 1),
        checkout=date(2026, 7, 10),
        adults=2,
    )

    print(f"Aantal live-resultaten: {len(results)}")
    for item in results[:5]:
        print(item.property_name, item.total_price, item.review_score_10, item.url)
