from __future__ import annotations

from datetime import date

from app.adapters.stays_booking import BookingStayAdapter
from app.config import get_settings
from app.destinations.seed_list import DESTINATIONS
from app.scraping.browser_manager import BrowserConfig, BrowserManager
from app.scraping.booking_url_builder import build_booking_search_url
from app.scraping.evidence import build_screenshot_path, write_json, write_text


if __name__ == "__main__":
    settings = get_settings()
    destination = DESTINATIONS[0]  # Alicante for first probe
    destination_query = destination.city
    checkin = date(2026, 7, 1)
    checkout = date(2026, 7, 10)
    adults = 2

    search_url = build_booking_search_url(destination_query, checkin, checkout, adults)
    screenshot_path = build_screenshot_path(settings.screenshot_dir, prefix="booking_probe")
    html_path = screenshot_path.with_suffix(".html")
    json_path = screenshot_path.with_suffix(".json")

    with BrowserManager(BrowserConfig(headless=True)) as manager:
        context = manager.new_context()
        page = context.new_page()
        page.goto(search_url, wait_until="domcontentloaded")
        page.screenshot(path=str(screenshot_path), full_page=True)
        html = page.content()
        title = page.title()
        context.close()

    write_text(html, html_path)

    adapter = BookingStayAdapter(headless=True, max_results=5)
    results = adapter.search_stays(
        destination_code=destination.arrival_airport,
        checkin=checkin,
        checkout=checkout,
        adults=adults,
    )

    payload = {
        "search_url": search_url,
        "title": title,
        "screenshot_path": str(screenshot_path),
        "html_path": str(html_path),
        "parsed_count": len(results),
        "sample_results": [
            {
                "property_name": r.property_name,
                "total_price": r.total_price,
                "review_score_10": r.review_score_10,
                "hotel_stars": r.hotel_stars,
                "source": r.source,
                "url": r.url,
            }
            for r in results[:5]
        ],
    }

    write_json(payload, json_path)
    print(payload)
