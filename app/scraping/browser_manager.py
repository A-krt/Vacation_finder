from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright


@dataclass(frozen=True)
class BrowserConfig:
    headless: bool = True
    browser_name: str = "chromium"
    viewport_width: int = 1440
    viewport_height: int = 1100
    navigation_timeout_ms: int = 60_000
    locale: str = "nl-NL"
    timezone_id: str = "Europe/Amsterdam"
    user_agent: Optional[str] = None


class BrowserManager:
    def __init__(self, config: BrowserConfig | None = None) -> None:
        self.config = config or BrowserConfig()
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None

    def start(self) -> None:
        if self._playwright is not None:
            return

        self._playwright = sync_playwright().start()
        browser_launcher = getattr(self._playwright, self.config.browser_name)
        self._browser = browser_launcher.launch(headless=self.config.headless)

    def stop(self) -> None:
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None

    def new_context(self) -> BrowserContext:
        if self._browser is None:
            raise RuntimeError("Browser is not started. Call start() first.")

        kwargs = {
            "viewport": {"width": self.config.viewport_width, "height": self.config.viewport_height},
            "locale": self.config.locale,
            "timezone_id": self.config.timezone_id,
        }
        if self.config.user_agent:
            kwargs["user_agent"] = self.config.user_agent

        context = self._browser.new_context(**kwargs)
        context.set_default_navigation_timeout(self.config.navigation_timeout_ms)
        context.set_default_timeout(self.config.navigation_timeout_ms)
        return context

    def new_page(self) -> Page:
        context = self.new_context()
        return context.new_page()

    def __enter__(self) -> "BrowserManager":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()
