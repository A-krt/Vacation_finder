from __future__ import annotations

import re
from typing import Iterable, TypeVar

T = TypeVar("T")


def normalize_property_name(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


def dedupe_by_lowest_price(items: Iterable[T], key_getter, price_getter):
    best = {}
    for item in items:
        key = key_getter(item)
        price = price_getter(item)
        if key not in best or price < price_getter(best[key]):
            best[key] = item
    return list(best.values())
