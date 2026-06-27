"""User profile (single-user: Gahan), DB-backed."""

from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User

router = APIRouter()


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    goals: Optional[str] = None
    experience_level: Optional[str] = None
    protein_target_g: Optional[int] = None
    football_day: Optional[str] = None
    weekly_split: Optional[List[str]] = None


def _serialize(u: User):
    return {
        "id": u.id,
        "email": u.email,
        "full_name": u.full_name,
        "location": u.location,
        "age": u.age,
        "height_cm": u.height_cm,
        "weight_kg": u.weight_kg,
        "gym_days_per_week": u.gym_days_per_week,
        "football_day": u.football_day,
        "goals": u.goals,
        "experience_level": u.experience_level,
        "protein_target_g": u.protein_target_g,
        "weekly_split": u.weekly_split,
    }


@router.get("/profile")
def get_user_profile(user: User = Depends(get_current_user)):
    return _serialize(user)


@router.put("/profile")
def update_user_profile(
    body: UserProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return _serialize(user)
