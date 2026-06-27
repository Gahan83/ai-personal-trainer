"""
Workout logging & progress tracking (V1 core).

- POST /workouts/{id}/complete : mark a session done (RPE, notes)
- POST /workouts/{id}/sets     : log a performed set
- GET  /workouts/history       : recent sessions
- GET  /workouts/progress      : per-exercise trends, PRs, plateau alerts
- POST /workouts/ai/generate   : ad-hoc AI workout (constraint-validated)
"""

from datetime import date
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User, WorkoutSession, SetLog
from app.services import trainer
from app.services.ai_service import ai_service

router = APIRouter(prefix="/workouts", tags=["workouts"])


class CompleteRequest(BaseModel):
    perceived_exertion: Optional[int] = None  # RPE 1-10
    notes: Optional[str] = None


class SetLogCreate(BaseModel):
    exercise: str
    set_number: int = 1
    reps: Optional[int] = None
    weight_kg: Optional[float] = None
    rpe: Optional[float] = None


class AIWorkoutRequest(BaseModel):
    day_type: str  # push|pull|legs|upper
    focus: Optional[str] = None
    minutes: int = 60


def _session_or_404(db: Session, user_id: int, session_id: int) -> WorkoutSession:
    s = (
        db.query(WorkoutSession)
        .filter(WorkoutSession.id == session_id, WorkoutSession.user_id == user_id)
        .first()
    )
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return s


def _serialize_session(s: WorkoutSession) -> Dict[str, Any]:
    return {
        "id": s.id,
        "date": s.date.isoformat(),
        "day_type": s.day_type,
        "title": s.title,
        "status": s.status,
        "perceived_exertion": s.perceived_exertion,
        "notes": s.notes,
        "sets": [
            {
                "exercise": x.exercise,
                "set_number": x.set_number,
                "reps": x.reps,
                "weight_kg": x.weight_kg,
                "rpe": x.rpe,
            }
            for x in s.set_logs
        ],
    }


@router.post("/{session_id}/complete")
def complete_session(
    session_id: int,
    body: CompleteRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = _session_or_404(db, user.id, session_id)
    s.status = "completed"
    if body.perceived_exertion is not None:
        s.perceived_exertion = body.perceived_exertion
    if body.notes is not None:
        s.notes = body.notes
    db.commit()
    db.refresh(s)
    return _serialize_session(s)


@router.post("/{session_id}/skip")
def skip_session(
    session_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = _session_or_404(db, user.id, session_id)
    s.status = "skipped"
    db.commit()
    return {"id": s.id, "status": s.status}


@router.post("/{session_id}/sets")
def log_set(
    session_id: int,
    body: SetLogCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = _session_or_404(db, user.id, session_id)
    # Guard: never log abs/core work.
    if trainer.validate_exercises([{"name": body.exercise}]):
        raise HTTPException(status_code=400, detail="Abs/core exercises are not allowed.")
    entry = SetLog(
        session_id=s.id,
        exercise=body.exercise,
        set_number=body.set_number,
        reps=body.reps,
        weight_kg=body.weight_kg,
        rpe=body.rpe,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"id": entry.id, "session_id": s.id, "exercise": entry.exercise}


@router.get("/history")
def history(
    limit: int = 20,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = (
        db.query(WorkoutSession)
        .filter(WorkoutSession.user_id == user.id)
        .order_by(WorkoutSession.date.desc(), WorkoutSession.id.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_session(s) for s in rows]


@router.get("/progress")
def progress(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Aggregate per-exercise trends: PR (max weight), total volume, and a
    naive plateau alert when the recent best hasn't beaten the older best."""
    rows = (
        db.query(SetLog)
        .join(WorkoutSession, SetLog.session_id == WorkoutSession.id)
        .filter(WorkoutSession.user_id == user.id)
        .order_by(SetLog.created_at.asc())
        .all()
    )

    by_ex: Dict[str, List[SetLog]] = {}
    for r in rows:
        by_ex.setdefault(r.exercise, []).append(r)

    exercises = []
    total_volume = 0.0
    for name, sets in by_ex.items():
        weights = [s.weight_kg for s in sets if s.weight_kg]
        volume = sum((s.weight_kg or 0) * (s.reps or 0) for s in sets)
        total_volume += volume
        pr = max(weights) if weights else None

        plateau = False
        if len(weights) >= 6:
            mid = len(weights) // 2
            older_best = max(weights[:mid])
            recent_best = max(weights[mid:])
            plateau = recent_best <= older_best
        exercises.append({
            "exercise": name,
            "pr_weight_kg": pr,
            "total_volume_kg": round(volume, 1),
            "sets_logged": len(sets),
            "plateau": plateau,
        })

    exercises.sort(key=lambda e: e["total_volume_kg"], reverse=True)
    completed = (
        db.query(WorkoutSession)
        .filter(WorkoutSession.user_id == user.id, WorkoutSession.status == "completed")
        .count()
    )
    return {
        "sessions_completed": completed,
        "total_volume_kg": round(total_volume, 1),
        "exercises": exercises,
        "plateau_alerts": [e["exercise"] for e in exercises if e["plateau"]],
    }


@router.post("/ai/generate")
def generate_ai_workout(
    req: AIWorkoutRequest,
    user: User = Depends(get_current_user),
):
    """AI-generated session, validated against the no-abs constraint. Falls back
    to the deterministic library plan if AI is unavailable."""
    if req.day_type not in trainer.GYM_TYPES:
        raise HTTPException(status_code=400, detail="day_type must be push, pull, legs, or upper.")

    base = trainer.build_session_plan(
        req.day_type, on=date.today(),
        split=user.weekly_split or trainer.DEFAULT_SPLIT,
    )

    if not ai_service.available:
        return {"source": "library", "plan": base}

    try:
        prompt = (
            f"Create a {req.minutes}-minute {req.day_type} workout for an "
            f"{user.experience_level} lifter. Focus: {req.focus or 'general'}. "
            "Return JSON: {\"exercises\":[{\"name\",\"sets\",\"reps\",\"rest\",\"cue\"}]}. "
            "Absolutely no abs/core exercises."
        )
        ai_plan = ai_service.generate_json(prompt)
        ai_ex = ai_plan.get("exercises", [])
        violations = trainer.validate_exercises(ai_ex)
        if violations:
            banned_names = {v.split(": ", 1)[-1] for v in violations}
            ai_ex = [e for e in ai_ex if e.get("name") not in banned_names]
        return {
            "source": "ai",
            "plan": {**base, "exercises": ai_ex or base["exercises"]},
            "removed_violations": violations,
        }
    except Exception as e:
        return {"source": "library", "plan": base, "ai_error": str(e)}
