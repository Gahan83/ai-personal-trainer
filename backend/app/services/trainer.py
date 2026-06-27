"""
Trainer domain logic: the deterministic brain behind the AI coach.

Holds the weekly split definition, a no-abs exercise library, the hard
constraint validator from the PRD, the weekly planner, and the adaptive
recovery engine. All pure Python so it works with zero AI/network access;
the AI layer (ai_service) only *enriches* what this produces.
"""

from __future__ import annotations

from typing import Dict, List, Any, Optional
from datetime import date

# Day-of-week codes, Monday-first (matches Python date.weekday(): Mon=0).
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

# Default weekly split (MON..SUN). The PRD's illustrative split puts legs the
# day before football, which violates its own constraint #4 — so we shift legs
# to Tuesday. Result is constraint-clean: 4 gym days, football Fri, 2 rest days.
DEFAULT_SPLIT = ["push", "legs", "rest", "pull", "football", "upper", "rest"]

# Day types considered hard CNS/lower-body load for spacing rules.
HARD_TYPES = {"legs", "football"}
GYM_TYPES = {"push", "pull", "legs", "upper"}

DAY_TYPE_META: Dict[str, Dict[str, Any]] = {
    "push": {"title": "Push · Chest / Shoulders / Triceps", "is_training": True},
    "pull": {"title": "Pull · Back / Biceps", "is_training": True},
    "legs": {"title": "Legs · Glutes / Quads / Hamstrings", "is_training": True},
    "upper": {"title": "Upper · Arms / Traps / Delts", "is_training": True},
    "football": {"title": "⚽ Football (active cardio + lower body)", "is_training": True},
    "rest": {"title": "Rest", "is_training": False},
}

# Curated exercise library. DELIBERATELY contains NO abs/core work — PRD hard
# constraint #1. Each entry: name, sets, reps, rest (sec), cue.
EXERCISE_LIBRARY: Dict[str, List[Dict[str, Any]]] = {
    "push": [
        {"name": "Barbell Bench Press", "sets": 4, "reps": "6-8", "rest": 150, "cue": "Retract scapula, controlled eccentric."},
        {"name": "Incline Dumbbell Press", "sets": 3, "reps": "8-10", "rest": 120, "cue": "Press slightly back over chest."},
        {"name": "Seated Overhead Press", "sets": 3, "reps": "8-10", "rest": 120, "cue": "Brace, no excessive lean back."},
        {"name": "Cable Flye", "sets": 3, "reps": "12-15", "rest": 75, "cue": "Soft elbows, squeeze at midline."},
        {"name": "Triceps Rope Pushdown", "sets": 3, "reps": "12-15", "rest": 60, "cue": "Lock elbows to sides."},
    ],
    "pull": [
        {"name": "Weighted Pull-up", "sets": 4, "reps": "6-8", "rest": 150, "cue": "Full hang to chin over bar."},
        {"name": "Barbell Row", "sets": 3, "reps": "8-10", "rest": 120, "cue": "Hinge ~45°, pull to lower ribs."},
        {"name": "Lat Pulldown", "sets": 3, "reps": "10-12", "rest": 90, "cue": "Drive elbows down and back."},
        {"name": "Seated Cable Row", "sets": 3, "reps": "10-12", "rest": 90, "cue": "Neutral spine, squeeze blades."},
        {"name": "Incline Dumbbell Curl", "sets": 3, "reps": "10-12", "rest": 60, "cue": "Full stretch at bottom."},
    ],
    "legs": [
        {"name": "Back Squat", "sets": 4, "reps": "5-8", "rest": 180, "cue": "Brace, knees track toes, depth to parallel."},
        {"name": "Romanian Deadlift", "sets": 3, "reps": "8-10", "rest": 150, "cue": "Hinge, bar close, feel hamstrings."},
        {"name": "Bulgarian Split Squat", "sets": 3, "reps": "8-10/leg", "rest": 120, "cue": "Stay tall, front-foot pressure."},
        {"name": "Leg Press", "sets": 3, "reps": "10-12", "rest": 120, "cue": "Don't lock out hard."},
        {"name": "Seated Leg Curl", "sets": 3, "reps": "12-15", "rest": 75, "cue": "Squeeze hamstrings, slow return."},
        {"name": "Standing Calf Raise", "sets": 4, "reps": "12-15", "rest": 60, "cue": "Full stretch and contraction."},
    ],
    "upper": [
        {"name": "Close-Grip Bench Press", "sets": 3, "reps": "8-10", "rest": 120, "cue": "Elbows tucked, triceps drive."},
        {"name": "Barbell Curl", "sets": 3, "reps": "8-10", "rest": 90, "cue": "No swinging, control down."},
        {"name": "Lateral Raise", "sets": 4, "reps": "12-15", "rest": 60, "cue": "Lead with elbows, slight lean."},
        {"name": "Barbell Shrug", "sets": 3, "reps": "12-15", "rest": 75, "cue": "Straight up, pause at top."},
        {"name": "Face Pull", "sets": 3, "reps": "15-20", "rest": 60, "cue": "Pull to forehead, rotate out."},
        {"name": "Hammer Curl", "sets": 3, "reps": "10-12", "rest": 60, "cue": "Neutral grip, brachialis focus."},
    ],
    "football": [
        {"name": "Dynamic Warm-up", "sets": 1, "reps": "10 min", "rest": 0, "cue": "Leg swings, lunges, sprints buildup."},
        {"name": "Match Play", "sets": 1, "reps": "60-90 min", "rest": 0, "cue": "Hydrate every break — Bangalore heat."},
        {"name": "Cooldown Walk + Stretch", "sets": 1, "reps": "10 min", "rest": 0, "cue": "Calves, quads, hip flexors."},
    ],
    "rest": [],
}


# ---------------------------------------------------------------------------
# Constraint engine
# ---------------------------------------------------------------------------

def validate_split(split: List[str]) -> List[str]:
    """Return a list of human-readable constraint violations. Empty = valid."""
    violations: List[str] = []
    n = len(split)

    for i, day_type in enumerate(split):
        day = DAYS[i] if i < len(DAYS) else f"day{i}"

        # #1 No abs/core — ever.
        if day_type in ("abs", "core"):
            violations.append(f"{day}: abs/core training is never allowed.")

        # #5 unknown types
        if day_type not in DAY_TYPE_META:
            violations.append(f"{day}: unknown day type '{day_type}'.")

        nxt = split[(i + 1) % n] if n else None

        # #4 Leg day not the day before football.
        if day_type == "legs" and nxt == "football":
            violations.append(f"{day}: leg day is scheduled the day before football.")

        # #3 At least one rest day between back-to-back hard sessions.
        if day_type in HARD_TYPES and nxt in HARD_TYPES:
            violations.append(
                f"{day}: two hard sessions ({day_type} → {nxt}) with no rest between."
            )

    # #2 Football is a training day — never a gym session the same day.
    # (Single slot per day makes this structurally impossible, but assert it.)
    if "football" in split:
        idx = split.index("football")
        if split[idx] in GYM_TYPES:
            violations.append("Gym session scheduled on football day.")

    return violations


def validate_exercises(exercises: List[Dict[str, Any]]) -> List[str]:
    """Reject any abs/core exercise that slipped into a plan."""
    banned = ("crunch", "sit-up", "sit up", "plank", "ab ", "abs", "core",
              "russian twist", "leg raise", "hollow", "v-up", "mountain climber")
    violations = []
    for ex in exercises:
        name = (ex.get("name") or "").lower()
        if any(b in name for b in banned):
            violations.append(f"Banned (abs/core) exercise: {ex.get('name')}")
    return violations


# ---------------------------------------------------------------------------
# Planning
# ---------------------------------------------------------------------------

def day_type_for(split: List[str], on: date) -> str:
    """Day type for a given calendar date based on the weekly split."""
    if not split:
        split = DEFAULT_SPLIT
    return split[on.weekday() % len(split)]


def week_overview(split: List[str]) -> List[Dict[str, Any]]:
    """Build the 7-day overview for the UI."""
    split = split or DEFAULT_SPLIT
    out = []
    for i, day in enumerate(DAYS):
        dt = split[i] if i < len(split) else "rest"
        meta = DAY_TYPE_META.get(dt, DAY_TYPE_META["rest"])
        out.append({
            "day": day,
            "day_type": dt,
            "title": meta["title"],
            "is_training": meta["is_training"],
        })
    return out


def _football_adjacency(split: List[str], on: date) -> Optional[str]:
    """Note football-day awareness: lighter the day before, recovery after."""
    if not split:
        split = DEFAULT_SPLIT
    n = len(split)
    today_idx = on.weekday() % n
    tomorrow = split[(today_idx + 1) % n]
    yesterday = split[(today_idx - 1) % n]
    if tomorrow == "football":
        return "Football tomorrow — keeping lower-body volume light to stay fresh."
    if yesterday == "football":
        return "Played football yesterday — lighter recovery focus today."
    return None


def build_session_plan(
    day_type: str,
    *,
    on: date,
    split: List[str],
    overload_hint: Optional[str] = None,
    readiness_note: Optional[str] = None,
) -> Dict[str, Any]:
    """Deterministic base plan for a day. AI enrichment is layered on top
    elsewhere; this guarantees a valid, constraint-safe plan with no AI."""
    meta = DAY_TYPE_META.get(day_type, DAY_TYPE_META["rest"])
    exercises = [dict(e) for e in EXERCISE_LIBRARY.get(day_type, [])]

    # Football-day awareness: trim leg volume the day before football.
    notes: List[str] = []
    adj = _football_adjacency(split, on)
    if adj:
        notes.append(adj)
    if day_type == "legs" and adj and "Football tomorrow" in adj:
        for e in exercises:
            if isinstance(e["sets"], int) and e["sets"] > 2:
                e["sets"] -= 1  # shave a set to reduce fatigue
        notes.append("Reduced one set per leg exercise.")

    if overload_hint:
        notes.append(overload_hint)
    if readiness_note:
        notes.append(readiness_note)

    # Constraint guard — never ship abs work.
    bad = validate_exercises(exercises)
    if bad:
        exercises = [e for e in exercises if e["name"] not in
                     [b.split(": ", 1)[-1] for b in bad]]

    est_minutes = sum(
        (e["sets"] if isinstance(e["sets"], int) else 1) * 2 for e in exercises
    ) if day_type != "football" else 90

    return {
        "day_type": day_type,
        "title": meta["title"],
        "is_training": meta["is_training"],
        "exercises": exercises,
        "estimated_minutes": est_minutes,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# Adaptive recovery engine
# ---------------------------------------------------------------------------

def adapt_today(
    day_type: str,
    *,
    soreness: Optional[int] = None,
    energy: Optional[int] = None,
    sore_muscles: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Given today's planned day type and a readiness check-in, decide whether
    to keep, deload, or swap to rest. Returns the (possibly changed) day_type
    plus a reason and a readiness note for the plan."""
    sore_muscles = sore_muscles or []
    soreness = soreness or 0
    energy = energy or 3

    result = {"day_type": day_type, "changed": False, "reason": None, "note": None}

    if day_type in ("rest", "football"):
        return result  # never override football or rest

    # Very sore overall, or low energy → convert hard day to active rest.
    if soreness >= 4 or energy <= 1:
        result.update({
            "day_type": "rest",
            "changed": True,
            "reason": "High soreness / low energy — swapping to a rest day to protect recovery.",
        })
        return result

    # Targeted muscle soreness on the matching day → deload.
    muscle_map = {
        "legs": {"legs", "quads", "hamstrings", "glutes", "calves"},
        "push": {"chest", "shoulders", "triceps"},
        "pull": {"back", "lats", "biceps"},
        "upper": {"arms", "traps", "shoulders", "biceps", "triceps"},
    }
    sore_set = {m.lower() for m in sore_muscles}
    if day_type in muscle_map and sore_set & muscle_map[day_type]:
        result["note"] = (
            f"Sore {', '.join(sore_set & muscle_map[day_type])} — deload ~10-15% "
            f"and stop 1-2 reps shy of failure."
        )
        return result

    # Feeling great → green light for a small overload.
    if energy >= 5 and soreness <= 1:
        result["note"] = "Feeling strong — aim to add weight or a rep vs last session."

    return result


def progressive_overload_hint(last_sets: List[Dict[str, Any]]) -> Optional[str]:
    """From the most recent logged sets of an exercise, suggest the next target."""
    if not last_sets:
        return None
    top = max(last_sets, key=lambda s: (s.get("weight_kg") or 0))
    w = top.get("weight_kg")
    reps = top.get("reps")
    name = top.get("exercise")
    if not (w and reps and name):
        return None
    if reps >= 10:
        return f"{name}: hit {reps} reps @ {w}kg last time — add ~2.5kg and aim for 6-8."
    return f"{name}: last {reps} reps @ {w}kg — try for +1 rep at the same load."
