from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo


def now_in_timezone(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


def timestamp_for_filename(timezone_name: str) -> str:
    return now_in_timezone(timezone_name).strftime("%Y-%m-%d_%H-%M-%S")
