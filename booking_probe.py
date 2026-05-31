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
    destination = DESTINATIONS[0]  # Alicante
    destination_query = destination.city
    checkin = date(2026, 7, 1)
    checkout = date(2026, 7, 10)
    adults = 2

    search_url = build_booking_search_url(destination_query, checkin, checkout, adults)
    screenshot_path = build_screenshot_path(settings.screenshot_dir, prefix="booking_probe")
    html_path = screenshot_path.with_suffix(".html")
    json_path = screenshot_path.with_suffix(".json")

    final_url = None
    title = None
    has_property_card = False
    parsed_results = []
    error_message = None

    with BrowserManager(BrowserConfig(headless=True)) as manager:
        context = manager.new_context()
        page = context.new_page()

        try:
            page.goto(search_url, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            error_message = f"Navigation error: {e}"

        final_url = page.url
        title = page.title()

        try:
            has_property_card = page.locator("[data-testid='property-card']").count() > 0
        except Exception:
            has_property_card = False

        page.screenshot(path=str(screenshot_path), full_page=True)
        html = page.content()
        write_text(html, html_path)

        context.close()

    try:
        adapter = BookingStayAdapter(headless=True, max_results=5)
        parsed_results = adapter.search_stays(
            destination_code=destination.arrival_airport,
            checkin=checkin,
            checkout=checkout,
            adults=adults,
        )
    except Exception as e:
        error_message = f"{error_message} | Parse error: {e}" if error_message else f"Parse error: {e}"

    payload = {
        "search_url": search_url,
        "final_url": final_url,
        "title": title,
        "has_property_card": has_property_card,
        "screenshot_path": str(screenshot_path),
        "html_path": str(html_path),
        "parsed_count": len(parsed_results),
        "error_message": error_message,
        "sample_results": [
            {
                "property_name": r.property_name,
                "total_price": r.total_price,
                "review_score_10": r.review_score_10,
                "hotel_stars": r.hotel_stars,
                "source": r.source,
                "url": r.url,
            }
            for r in parsed_results[:5]
        ],
    }

    write_json(payload, json_path)
    print(payload)
