from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StaySiteConfig:
    name: str
    base_url: str
    result_card: str
    property_name: str
    property_link: str | None
    property_type: str | None
    total_price: str
    review_text: str | None
    stars_text: str | None
    private_bathroom_text: str | None
    bed_text: str | None
    cookie_accept_button: str | None = None
    load_more_button: str | None = None
    next_page_button: str | None = None
    search_url_builder_name: str = "template"
    metadata: dict[str, str] = field(default_factory=dict)


# BELANGRIJK:
# Dit is nog een placeholder-config.
# Deze moeten we later vervangen door selectors van een echte site.
DEFAULT_STAY_SITE_CONFIG = StaySiteConfig(
    name="PLACEHOLDER_SITE",
    base_url="https://example.com",
    result_card="article[data-testid='property-card']",
    property_name="[data-testid='title']",
    property_link="a",
    property_type="[data-testid='property-type']",
    total_price="[data-testid='price-and-discounted-price']",
    review_text="[data-testid='review-score']",
    stars_text="[aria-label*='star']",
    private_bathroom_text="body",
    bed_text="body",
    cookie_accept_button=None,
    load_more_button=None,
    next_page_button=None,
    search_url_builder_name="template",
)
