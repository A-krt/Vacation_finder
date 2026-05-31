from __future__ import annotations

from dataclasses import dataclass

from app.config import get_settings
from app.scraping.browser_manager import BrowserConfig, BrowserManager
from app.scraping.evidence import build_screenshot_path, write_json


@dataclass(frozen=True)
class ProbeResult:
    url: str
    title: str
    screenshot_path: str
    metadata_path: str


def run_browser_probe(target_url: str = "https://example.com") -> ProbeResult:
    settings = get_settings()
    screenshot_path = build_screenshot_path(settings.screenshot_dir, prefix="browser_probe")
    metadata_path = screenshot_path.with_suffix(".json")

    config = BrowserConfig(headless=True)

    with BrowserManager(config) as manager:
        page = manager.new_page()
        page.goto(target_url, wait_until="domcontentloaded")
        page.screenshot(path=str(screenshot_path), full_page=True)
        title = page.title()
        page.context.close()

    result = ProbeResult(
        url=target_url,
        title=title,
        screenshot_path=str(screenshot_path),
        metadata_path=str(metadata_path),
    )
    write_json(result, metadata_path)
    return result
