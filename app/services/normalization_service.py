from __future__ import annotations

from typing import Optional


def normalize_review_score_to_10(review_5: float | None, review_10: float | None) -> Optional[float]:
    candidates: list[float] = []
    if review_5 is not None:
        candidates.append(round(review_5 * 2, 2))
    if review_10 is not None:
        candidates.append(round(review_10, 2))
    return max(candidates) if candidates else None


def hotel_stars_to_quality_score(stars: float | None) -> Optional[float]:
    if stars is None:
        return None
    return round((stars / 5.0) * 10.0, 2)


def get_best_quality_score(
    hotel_stars: float | None,
    review_5: float | None,
    review_10: float | None,
) -> Optional[float]:
    candidates: list[float] = []
    star_score = hotel_stars_to_quality_score(hotel_stars)
    review_score = normalize_review_score_to_10(review_5, review_10)

    if star_score is not None:
        candidates.append(star_score)
    if review_score is not None:
        candidates.append(review_score)

    return max(candidates) if candidates else None
