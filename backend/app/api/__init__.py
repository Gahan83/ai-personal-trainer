from fastapi import APIRouter
from app.api.endpoints import auth, users, workouts, exercises, mcp

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(mcp.router, tags=["mcp"])