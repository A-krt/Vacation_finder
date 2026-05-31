from __future__ import annotations

import re
from typing import Optional


def parse_price_to_float(text: str | None) -> Optional[float]:
    if not text:
        return None

    cleaned = text.strip()
    cleaned = cleaned.replace("€", "").replace("EUR", "").replace("\u00a0", " ")
    cleaned = cleaned.replace("per night", "").replace("per nacht", "")
    cleaned = cleaned.replace("totaal", "").replace("total", "")
    cleaned = re.sub(r"[^0-9,\.]", "", cleaned)

    if not cleaned:
        return None

    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")

    try:
        return round(float(cleaned), 2)
    except ValueError:
        return None


def parse_review_score(text: str | None) -> tuple[float | None, float | None]:
    if not text:
        return None, None

    cleaned = text.strip().lower().replace(",", ".")
    numbers = re.findall(r"\d+(?:\.\d+)?", cleaned)
    if not numbers:
        return None, None

    score = float(numbers[0])

    if "/5" in cleaned or "out of 5" in cleaned:
        return round(score, 2), round(score * 2, 2)

    if "/10" in cleaned or "out of 10" in cleaned:
        return round(score / 2, 2), round(score, 2)

    if score <= 5:
        return round(score, 2), round(score * 2, 2)

    return round(score / 2, 2), round(score, 2)


def parse_hotel_stars(text: str | None) -> float | None:
    if not text:
        return None

    cleaned = text.strip().lower().replace(",", ".")
    match = re.search(r"(\d+(?:\.\d+)?)", cleaned)
    if not match:
        return None

    value = float(match.group(1))
    if 0 < value <= 5.0:
        return round(value, 2)

    return None
