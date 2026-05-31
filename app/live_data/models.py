from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ProviderAttempt:
    provider_name: str
    success: bool
    blocked: bool = False
    results_count: int = 0
    error_message: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class SearchAudit:
    search_timestamp: datetime
    category: str
    attempts: list[ProviderAttempt] = field(default_factory=list)

    def add_attempt(self, attempt: ProviderAttempt) -> None:
        self.attempts.append(attempt)
