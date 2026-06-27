"""
Database bootstrap: create tables and seed the single Gahan user on startup.
Idempotent — safe to call every boot.
"""

from app.core.database import Base, engine, SessionLocal
from app.models.models import User
from app.services.trainer import DEFAULT_SPLIT

# Single-user app: Gahan is always user id 1.
GAHAN_USER_ID = 1


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == GAHAN_USER_ID).first()
        if user is None:
            user = User(
                id=GAHAN_USER_ID,
                email="gahan899@gmail.com",
                full_name="Gahan",
                location="Bangalore",
                gym_days_per_week=4,
                football_day="FRI",
                goals="physique, strength, longevity",
                experience_level="intermediate",
                protein_target_g=140,
                weekly_split=list(DEFAULT_SPLIT),
            )
            db.add(user)
            db.commit()
        elif not user.weekly_split:
            user.weekly_split = list(DEFAULT_SPLIT)
            db.commit()
    finally:
        db.close()
