from fastapi import APIRouter
from app.api.endpoints import (
    auth, users, workouts, exercises, mcp,
    agent, checkin, nutrition, wearables,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])

# These routers declare their own prefixes internally.
api_router.include_router(workouts.router)
api_router.include_router(agent.router)
api_router.include_router(checkin.router)
api_router.include_router(nutrition.router)
api_router.include_router(wearables.router)
api_router.include_router(mcp.router)
