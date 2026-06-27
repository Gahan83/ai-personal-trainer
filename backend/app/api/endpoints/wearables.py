"""
Wearable / health data sync (V3).

Real Apple Health / Google Fit / Fitbit OAuth is out of scope here; this
exposes a manual/ingest endpoint with the same shape those integrations would
push, plus a recovery readout derived from the latest metrics.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User, WearableData

router = APIRouter(prefix="/wearables", tags=["wearables"])


class WearableCreate(BaseModel):
    source: str = "manual"  # apple_health | google_fit | fitbit | manual
    sleep_hours: Optional[float] = None
    hrv_ms: Optional[float] = None
    resting_hr: Optional[int] = None
    steps: Optional[int] = None


def _serialize(w: WearableData):
    return {
        "id": w.id,
        "date": w.date.isoformat(),
        "source": w.source,
        "sleep_hours": w.sleep_hours,
        "hrv_ms": w.hrv_ms,
        "resting_hr": w.resting_hr,
        "steps": w.steps,
    }


def _recovery_readout(w: Optional[WearableData]) -> dict:
    """Crude recovery score from sleep + HRV to inform recommendations."""
    if not w:
        return {"score": None, "advice": "No wearable data yet. Connect a device or log manually."}
    score = 50
    if w.sleep_hours is not None:
        score += min(25, max(-25, (w.sleep_hours - 7) * 10))
    if w.hrv_ms is not None:
        score += min(25, max(-25, (w.hrv_ms - 60) * 0.5))
    score = int(max(0, min(100, score)))
    if score >= 75:
        advice = "Well recovered — good day to push intensity."
    elif score >= 50:
        advice = "Moderate recovery — train as planned, watch RPE."
    else:
        advice = "Low recovery — consider a deload or extra rest."
    return {"score": score, "advice": advice}


@router.get("/latest")
def latest(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    w = (
        db.query(WearableData)
        .filter(WearableData.user_id == user.id)
        .order_by(WearableData.date.desc(), WearableData.id.desc())
        .first()
    )
    return {
        "data": _serialize(w) if w else None,
        "recovery": _recovery_readout(w),
    }


@router.post("/sync")
def sync(
    body: WearableCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    today = date.today()
    w = (
        db.query(WearableData)
        .filter(WearableData.user_id == user.id, WearableData.date == today)
        .first()
    )
    if w is None:
        w = WearableData(user_id=user.id, date=today)
        db.add(w)
    w.source = body.source
    for field in ("sleep_hours", "hrv_ms", "resting_hr", "steps"):
        val = getattr(body, field)
        if val is not None:
            setattr(w, field, val)
    db.commit()
    db.refresh(w)
    return {"data": _serialize(w), "recovery": _recovery_readout(w)}
