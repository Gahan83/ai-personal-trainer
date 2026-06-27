"""Exercise library — served from the curated no-abs library in trainer.py."""

from typing import Optional

from fastapi import APIRouter, Query

from app.services.trainer import EXERCISE_LIBRARY, DAY_TYPE_META

router = APIRouter()


@router.get("/")
def get_exercises(day_type: Optional[str] = Query(None, description="push|pull|legs|upper|football")):
    """Flat list of exercises, optionally filtered by day type. No abs — ever."""
    out = []
    for dt, items in EXERCISE_LIBRARY.items():
        if day_type and dt != day_type:
            continue
        for e in items:
            out.append({**e, "day_type": dt})
    return out


@router.get("/day-types")
def get_day_types():
    return [
        {"day_type": dt, **meta, "exercise_count": len(EXERCISE_LIBRARY.get(dt, []))}
        for dt, meta in DAY_TYPE_META.items()
    ]
