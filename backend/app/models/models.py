"""
SQLAlchemy ORM models for the AI Personal Trainer.

Single-user app (Gahan), but a User row still anchors all data so the schema
can extend to multi-user later without migration pain.
"""

from datetime import datetime, date

from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime, Text, ForeignKey, JSON
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    location = Column(String, default="Bangalore")

    age = Column(Integer, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)

    gym_days_per_week = Column(Integer, default=4)
    football_day = Column(String, default="FRI")  # day-of-week code
    goals = Column(String, default="physique, strength, longevity")
    experience_level = Column(String, default="intermediate")
    protein_target_g = Column(Integer, default=140)

    # Ordered list of day_type strings for the weekly split, e.g.
    # ["push","pull","rest","legs","football","upper","rest"] (MON..SUN)
    weekly_split = Column(JSON, default=list)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sessions = relationship("WorkoutSession", back_populates="user", cascade="all, delete-orphan")
    checkins = relationship("CheckIn", back_populates="user", cascade="all, delete-orphan")
    nutrition = relationship("NutritionLog", back_populates="user", cascade="all, delete-orphan")
    wearables = relationship("WearableData", back_populates="user", cascade="all, delete-orphan")


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=date.today, index=True)

    day_type = Column(String, nullable=False)   # push|pull|legs|upper|football|rest
    title = Column(String, nullable=True)        # e.g. "Push · Chest / Shoulders"
    status = Column(String, default="planned")   # planned|completed|skipped
    perceived_exertion = Column(Integer, nullable=True)  # RPE 1-10 for the session
    notes = Column(Text, nullable=True)
    # Full AI-generated plan snapshot (exercises/sets/reps/rest/cues)
    plan = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
    set_logs = relationship("SetLog", back_populates="session", cascade="all, delete-orphan")


class SetLog(Base):
    __tablename__ = "set_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False)
    exercise = Column(String, nullable=False, index=True)
    set_number = Column(Integer, default=1)
    reps = Column(Integer, nullable=True)
    weight_kg = Column(Float, nullable=True)
    rpe = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("WorkoutSession", back_populates="set_logs")


class CheckIn(Base):
    """Daily 30-second readiness check-in feeding the adaptive engine."""
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=date.today, index=True)

    soreness = Column(Integer, nullable=True)   # 1 (none) .. 5 (very sore)
    energy = Column(Integer, nullable=True)      # 1 (drained) .. 5 (great)
    sleep_hours = Column(Float, nullable=True)
    sore_muscles = Column(JSON, default=list)    # e.g. ["legs","chest"]
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="checkins")


class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=date.today, index=True)

    protein_g = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)
    water_ml = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="nutrition")


class WearableData(Base):
    """V3: pulled/entered health metrics for smarter recovery."""
    __tablename__ = "wearable_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=date.today, index=True)

    source = Column(String, default="manual")   # apple_health|google_fit|fitbit|manual
    sleep_hours = Column(Float, nullable=True)
    hrv_ms = Column(Float, nullable=True)
    resting_hr = Column(Integer, nullable=True)
    steps = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wearables")
