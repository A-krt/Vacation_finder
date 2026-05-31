from __future__ import annotations

from app.scraping.selectors import StaySiteConfig


# NOTE:
# Dit zijn eerste Expedia selector-hypotheses.
# Deze zullen waarschijnlijk nog tuning nodig hebben na de eerste expedia_probe artifacts.
EXPEDIA_STAY_SITE_CONFIG = StaySiteConfig(
    name="expedia",
    base_url="https://www.expedia.com/Hotel-Search",
    result_card="[data-stid='property-listing-results'] > li, section[data-stid='property-listing']",
    property_name="[data-stid='content-hotel-title'], [data-stid='open-hotel-information']",
    property_link="a[data-stid='open-hotel-information'], a[href*='Hotel-Information']",
    property_type="[data-stid='property-type-info']",
    total_price="[data-stid='price-lockup-text'], [data-stid='price-summary-message-line'], [data-test-id='price-summary-message-line']",
    review_text="[data-stid='content-hotel-review-summary'], [data-stid='content-hotel-reviews-superlative']",
    stars_text="[aria-label*='star'], [aria-label*='stars']",
    private_bathroom_text="body",
    bed_text="body",
    cookie_accept_button="button[id*='onetrust-accept'], button[aria-label*='Accept'], button[aria-label*='accept']",
    load_more_button="button[data-stid='show-more-results'], button[aria-label*='Show more results']",
    next_page_button="button[aria-label*='Next'], a[aria-label*='Next']",
    search_url_builder_name="expedia_search_results",
)
