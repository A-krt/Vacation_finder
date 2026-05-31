from __future__ import annotations

from app.models import Destination


DESTINATIONS: list[Destination] = [
    Destination("ALC", "Alicante", "Spain", "ALC", 8.8, ["beach", "city", "restaurants", "bars"]),
    Destination("AGP", "Malaga", "Spain", "AGP", 9.0, ["beach", "city", "restaurants", "bars"]),
    Destination("VLC", "Valencia", "Spain", "VLC", 8.7, ["beach", "city", "restaurants", "bars"]),
    Destination("PMI", "Palma de Mallorca", "Spain", "PMI", 8.9, ["beach", "city", "restaurants", "bars"]),
    Destination("FAO", "Faro", "Portugal", "FAO", 8.2, ["beach", "city", "restaurants", "bars"]),
    Destination("LIS", "Lisbon", "Portugal", "LIS", 8.5, ["city", "restaurants", "bars"]),
    Destination("NAP", "Naples", "Italy", "NAP", 8.0, ["city", "restaurants", "bars"]),
    Destination("CTA", "Catania", "Italy", "CTA", 8.6, ["beach", "city", "restaurants", "bars"]),
    Destination("BRI", "Bari", "Italy", "BRI", 8.1, ["beach", "city", "restaurants", "bars"]),
    Destination("NCE", "Nice", "France", "NCE", 8.4, ["beach", "city", "restaurants", "bars"]),
    Destination("SPU", "Split", "Croatia", "SPU", 8.5, ["beach", "city", "restaurants", "bars"]),
    Destination("DBV", "Dubrovnik", "Croatia", "DBV", 8.3, ["beach", "city", "restaurants", "bars"]),
    Destination("HER", "Heraklion", "Greece", "HER", 8.4, ["beach", "restaurants", "bars"]),
    Destination("CHQ", "Chania", "Greece", "CHQ", 8.7, ["beach", "restaurants", "bars"]),
    Destination("RHO", "Rhodes", "Greece", "RHO", 8.5, ["beach", "restaurants", "bars"]),
    Destination("MLA", "Malta", "Malta", "MLA", 8.6, ["beach", "city", "restaurants", "bars"]),
    Destination("LCA", "Larnaca", "Cyprus", "LCA", 8.4, ["beach", "city", "restaurants", "bars"]),
    Destination("PFO", "Paphos", "Cyprus", "PFO", 8.3, ["beach", "restaurants", "bars"]),
]
