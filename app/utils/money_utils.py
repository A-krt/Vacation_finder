from __future__ import annotations


def fmt_eur(amount: float) -> str:
    return f"€{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
