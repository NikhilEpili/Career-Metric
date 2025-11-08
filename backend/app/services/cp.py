from __future__ import annotations

from statistics import mean
from typing import Iterable


def aggregate_cp_ratings(ratings: Iterable[int]) -> dict:
    rating_list = list(ratings)
    if not rating_list:
        return {"average": 0, "attempts": 0}

    return {"average": round(mean(rating_list), 2), "attempts": len(rating_list)}
