"""Daily readiness check-in (V2 adaptive recovery engine input)."""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User, CheckIn

router = APIRouter(prefix="/checkin", tags=["checkin"])


class CheckInCreate(BaseModel):
    soreness: int = Field(ge=1, le=5, description="1 none .. 5 very sore")
    energy: int = Field(ge=1, le=5, description="1 drained .. 5 great")
    sleep_hours: Optional[float] = None
    sore_muscles: List[str] = []
    notes: Optional[str] = None


def _serialize(c: CheckIn):
    return {
        "id": c.id,
        "date": c.date.isoformat(),
        "soreness": c.soreness,
        "energy": c.energy,
        "sleep_hours": c.sleep_hours,
        "sore_muscles": c.sore_muscles or [],
        "notes": c.notes,
    }


@router.get("/today")
def get_today_checkin(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    c = (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user.id, CheckIn.date == date.today())
        .order_by(CheckIn.id.desc())
        .first()
    )
    return _serialize(c) if c else None


@router.post("/")
def submit_checkin(
    body: CheckInCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    today = date.today()
    c = (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user.id, CheckIn.date == today)
        .first()
    )
    if c is None:
        c = CheckIn(user_id=user.id, date=today)
        db.add(c)
    c.soreness = body.soreness
    c.energy = body.energy
    c.sleep_hours = body.sleep_hours
    c.sore_muscles = body.sore_muscles
    c.notes = body.notes
    db.commit()
    db.refresh(c)
    return _serialize(c)


@router.get("/history")
def checkin_history(
    limit: int = 14,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user.id)
        .order_by(CheckIn.date.desc())
        .limit(limit)
        .all()
    )
    return [_serialize(c) for c in rows]
