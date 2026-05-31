from __future__ import annotations

from app.scraping.site_probe import run_browser_probe


if __name__ == "__main__":
    result = run_browser_probe()
    print(f"Browser probe gelukt: {result.title}")
    print(f"Screenshot opgeslagen op: {result.screenshot_path}")
    print(f"Metadata opgeslagen op: {result.metadata_path}")
