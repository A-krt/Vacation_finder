from __future__ import annotations

from app.scraping.selectors import StaySiteConfig


# NOTE:
# These selectors are an initial Booking.com hypothesis and may need to be adjusted
# after inspecting the HTML and screenshots produced by booking_probe.py.
BOOKING_STAY_SITE_CONFIG = StaySiteConfig(
    name="booking.com",
    base_url="https://www.booking.com/searchresults.html",
    result_card="[data-testid='property-card']",
    property_name="[data-testid='title']",
    property_link="a[data-testid='title-link'], a[data-testid='property-card-desktop-single-image']",
    property_type="[data-testid='property-card-unit-configuration']",
    total_price="[data-testid='price-and-discounted-price'], [data-testid='price-and-discounted-price'] span, [data-testid='price-and-discounted-price'] div",
    review_text="[data-testid='review-score']",
    stars_text="[aria-label*='out of 5'], [aria-label*='stars'], [aria-label*='sterren']",
    private_bathroom_text="body",
    bed_text="body",
    cookie_accept_button="#onetrust-accept-btn-handler, button[aria-label*='Accept'], button[aria-label*='Accepteren']",
    load_more_button=None,
    next_page_button="button[aria-label*='Next page'], button[aria-label*='Volgende pagina']",
    search_url_builder_name="booking_search_results",
)
