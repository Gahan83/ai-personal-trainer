"""
Agent endpoints — the AI coach surface.

- GET  /agent/today : today's adaptive workout suggestion (V1 + V2 adaptive)
- GET  /agent/week  : weekly split overview + constraint check
- POST /agent/chat  : conversational guidance, context-aware (V1)
"""

from datetime import date
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User, WorkoutSession, SetLog, CheckIn
from app.services import trainer
from app.services.ai_service import ai_service

router = APIRouter(prefix="/agent", tags=["agent"])


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


def _latest_checkin(db: Session, user_id: int, on: date) -> Optional[CheckIn]:
    return (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user_id, CheckIn.date == on)
        .order_by(CheckIn.id.desc())
        .first()
    )


def _overload_hint(db: Session, user_id: int, day_type: str) -> Optional[str]:
    """Pull the last completed session of this day type and suggest progression."""
    last = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.day_type == day_type,
            WorkoutSession.status == "completed",
        )
        .order_by(WorkoutSession.date.desc())
        .first()
    )
    if not last:
        return None
    sets = [
        {"exercise": s.exercise, "reps": s.reps, "weight_kg": s.weight_kg}
        for s in last.set_logs
    ]
    return trainer.progressive_overload_hint(sets)


@router.get("/week")
def get_week(user: User = Depends(get_current_user)):
    split = user.weekly_split or trainer.DEFAULT_SPLIT
    return {
        "split": split,
        "overview": trainer.week_overview(split),
        "violations": trainer.validate_split(split),
    }


@router.get("/today")
def get_today(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    today = date.today()
    split = user.weekly_split or trainer.DEFAULT_SPLIT
    planned_type = trainer.day_type_for(split, today)

    # Adaptive recovery engine — adjust based on today's check-in.
    checkin = _latest_checkin(db, user.id, today)
    adapt = trainer.adapt_today(
        planned_type,
        soreness=checkin.soreness if checkin else None,
        energy=checkin.energy if checkin else None,
        sore_muscles=checkin.sore_muscles if checkin else None,
    )
    day_type = adapt["day_type"]

    overload = _overload_hint(db, user.id, day_type) if day_type in trainer.GYM_TYPES else None
    plan = trainer.build_session_plan(
        day_type,
        on=today,
        split=split,
        overload_hint=overload,
        readiness_note=adapt.get("note"),
    )

    # Persist/refresh today's session snapshot.
    session = (
        db.query(WorkoutSession)
        .filter(WorkoutSession.user_id == user.id, WorkoutSession.date == today)
        .first()
    )
    if session is None:
        session = WorkoutSession(
            user_id=user.id, date=today, day_type=day_type,
            title=plan["title"], status="planned", plan=plan,
        )
        db.add(session)
    else:
        session.day_type = day_type
        session.title = plan["title"]
        session.plan = plan
    db.commit()
    db.refresh(session)

    # Optional AI coach note (graceful if Azure not configured).
    coach_note = None
    if ai_service.available and plan["is_training"]:
        try:
            ex_names = ", ".join(e["name"] for e in plan["exercises"][:6])
            prompt = (
                f"Today is {day_type} day. Plan: {ex_names}. "
                f"{adapt.get('reason') or ''} {adapt.get('note') or ''} "
                "Give a 2-sentence motivating coaching note. No abs work."
            )
            coach_note = ai_service.generate_completion(prompt, max_tokens=150)
        except Exception:
            coach_note = None

    return {
        "date": today.isoformat(),
        "planned_day_type": planned_type,
        "adapted": adapt["changed"],
        "adaptation_reason": adapt.get("reason"),
        "session_id": session.id,
        "status": session.status,
        "plan": plan,
        "coach_note": coach_note,
        "checked_in": checkin is not None,
        "ai_enabled": ai_service.available,
    }


@router.post("/chat")
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not ai_service.available:
        raise HTTPException(
            status_code=503,
            detail="AI not configured. Set OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in backend/.env.",
        )

    today = date.today()
    split = user.weekly_split or trainer.DEFAULT_SPLIT
    day_type = trainer.day_type_for(split, today)
    checkin = _latest_checkin(db, user.id, today)

    context = (
        f"User: {user.full_name}, {user.experience_level}, goals: {user.goals}. "
        f"Today is {day_type} day. "
    )
    if checkin:
        context += (
            f"Check-in today: soreness {checkin.soreness}/5, energy {checkin.energy}/5"
            f"{', sore: ' + ', '.join(checkin.sore_muscles) if checkin.sore_muscles else ''}. "
        )

    messages: List[Dict[str, Any]] = [
        {"role": "user", "content": f"[context] {context}"},
    ]
    for m in req.history[-8:]:
        messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": req.message})

    try:
        reply = ai_service.chat(messages, max_tokens=600)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {e}")

    return {"reply": reply, "day_type": day_type}
