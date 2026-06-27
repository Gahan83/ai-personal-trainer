"""Shared API dependencies."""

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.seed import GAHAN_USER_ID
from app.models.models import User


def get_current_user(db: Session = Depends(get_db)) -> User:
    """Single-user app — always returns Gahan. Swap for real auth later."""
    user = db.query(User).filter(User.id == GAHAN_USER_ID).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found. DB not seeded.")
    return user
