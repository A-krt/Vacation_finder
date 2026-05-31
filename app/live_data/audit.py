from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from app.live_data.models import SearchAudit


def write_audit_file(audit: SearchAudit, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(audit), ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return output_path
