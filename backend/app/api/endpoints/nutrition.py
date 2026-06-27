"""Nutrition & hydration nudges (V2). Simple guidance, not a meal-plan engine."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User, NutritionLog
from app.services import trainer

router = APIRouter(prefix="/nutrition", tags=["nutrition"])


class NutritionCreate(BaseModel):
    protein_g: Optional[float] = None
    calories: Optional[float] = None
    water_ml: Optional[float] = None
    notes: Optional[str] = None


def _serialize(n: NutritionLog):
    return {
        "id": n.id,
        "date": n.date.isoformat(),
        "protein_g": n.protein_g,
        "calories": n.calories,
        "water_ml": n.water_ml,
        "notes": n.notes,
    }


# Static, training-type-aware nudges. Keeps V2 simple per the PRD.
NUDGES = {
    "push": "Pre: carbs + coffee 60-90 min out. Post: 30-40g protein + carbs within an hour.",
    "pull": "Prioritise protein today for back/biceps recovery. 30-40g post-session.",
    "legs": "Fuel up — carbs before legs. Extra protein + water after; expect appetite spike.",
    "upper": "Light pre-workout snack is enough. Hit your protein target across the day.",
    "football": "Hydrate hard — 500ml before, sip every break (Bangalore heat). Carbs before, protein + fluids after.",
    "rest": "Recovery day: hold protein target, plenty of water, prioritise sleep.",
}


@router.get("/nudges")
def get_nudges(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    split = user.weekly_split or trainer.DEFAULT_SPLIT
    day_type = trainer.day_type_for(split, date.today())
    today = (
        db.query(NutritionLog)
        .filter(NutritionLog.user_id == user.id, NutritionLog.date == date.today())
        .first()
    )
    protein_logged = today.protein_g if today and today.protein_g else 0
    return {
        "day_type": day_type,
        "guidance": NUDGES.get(day_type, NUDGES["rest"]),
        "protein_target_g": user.protein_target_g,
        "protein_logged_g": protein_logged,
        "protein_remaining_g": max(0, (user.protein_target_g or 0) - protein_logged),
        "hydrate_extra": day_type == "football",
    }


@router.post("/")
def log_nutrition(
    body: NutritionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    today = date.today()
    n = (
        db.query(NutritionLog)
        .filter(NutritionLog.user_id == user.id, NutritionLog.date == today)
        .first()
    )
    if n is None:
        n = NutritionLog(user_id=user.id, date=today)
        db.add(n)
    # Accumulate protein/water/calories across the day; replace notes.
    if body.protein_g is not None:
        n.protein_g = (n.protein_g or 0) + body.protein_g
    if body.calories is not None:
        n.calories = (n.calories or 0) + body.calories
    if body.water_ml is not None:
        n.water_ml = (n.water_ml or 0) + body.water_ml
    if body.notes is not None:
        n.notes = body.notes
    db.commit()
    db.refresh(n)
    return _serialize(n)
