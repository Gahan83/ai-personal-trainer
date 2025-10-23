from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

router = APIRouter()

class UserProfile(BaseModel):
    id: int
    email: str
    full_name: str
    age: Optional[int] = None
    height: Optional[float] = None  # in cm
    weight: Optional[float] = None  # in kg
    fitness_goal: Optional[str] = None
    experience_level: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    fitness_goal: Optional[str] = None
    experience_level: Optional[str] = None

@router.get("/profile", response_model=UserProfile, summary="Get User Profile", description="Retrieve the current user's profile information")
async def get_user_profile():
    """
    Get user profile
    
    Returns the current user's profile information including personal details and fitness preferences
    """
    # TODO: Implement user profile retrieval from database
    # This would typically require authentication to get the current user
    return {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe",
        "age": 28,
        "height": 175.0,
        "weight": 70.0,
        "fitness_goal": "Build muscle",
        "experience_level": "intermediate",
        "created_at": "2024-01-01T10:00:00",
        "updated_at": "2024-01-01T10:00:00"
    }

@router.put("/profile", response_model=UserProfile, summary="Update User Profile", description="Update the current user's profile information")
async def update_user_profile(profile_update: UserProfileUpdate):
    """
    Update user profile
    
    - **full_name**: User's full name
    - **age**: User's age
    - **height**: User's height in cm
    - **weight**: User's weight in kg
    - **fitness_goal**: User's fitness goal (build muscle, lose weight, etc.)
    - **experience_level**: User's fitness experience level
    
    Returns the updated profile information
    """
    # TODO: Implement user profile update in database
    # This would typically require authentication to get the current user
    
    # Simulate updating the profile
    updated_profile = {
        "id": 1,
        "email": "user@example.com",
        "full_name": profile_update.full_name or "John Doe",
        "age": profile_update.age or 28,
        "height": profile_update.height or 175.0,
        "weight": profile_update.weight or 70.0,
        "fitness_goal": profile_update.fitness_goal or "Build muscle",
        "experience_level": profile_update.experience_level or "intermediate",
        "created_at": "2024-01-01T10:00:00",
        "updated_at": "2024-01-01T12:00:00"
    }
    
    return updated_profile
