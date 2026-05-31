from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def timestamp_for_file() -> str:
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def build_screenshot_path(base_dir: Path, prefix: str = "probe") -> Path:
    ensure_dir(base_dir)
    return base_dir / f"{prefix}_{timestamp_for_file()}.png"


def write_json(data: Any, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    serializable = asdict(data) if is_dataclass(data) else data
    output_path.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path
