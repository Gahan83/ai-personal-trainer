from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Exercise(BaseModel):
    id: int
    name: str
    description: str
    category: str
    muscle_groups: List[str]
    equipment: Optional[str] = None
    difficulty: str
    instructions: List[str]

class ExerciseCategory(BaseModel):
    id: int
    name: str
    description: str
    exercise_count: int

@router.get("/", response_model=List[Exercise], summary="Get All Exercises", description="Retrieve all available exercises with optional filtering")
async def get_exercises(
    category: Optional[str] = Query(None, description="Filter by exercise category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    muscle_group: Optional[str] = Query(None, description="Filter by muscle group")
):
    """
    Get all exercises with optional filtering
    
    - **category**: Filter by exercise category (chest, back, legs, etc.)
    - **difficulty**: Filter by difficulty (beginner, intermediate, advanced)
    - **muscle_group**: Filter by muscle group (chest, back, shoulders, etc.)
    """
    # TODO: Implement exercise retrieval from database with filtering
    sample_exercises = [
        {
            "id": 1,
            "name": "Push-ups",
            "description": "Classic bodyweight exercise for chest, shoulders, and triceps",
            "category": "strength",
            "muscle_groups": ["chest", "shoulders", "triceps"],
            "equipment": None,
            "difficulty": "beginner",
            "instructions": [
                "Start in a plank position with hands slightly wider than shoulders",
                "Lower your body until chest nearly touches the floor",
                "Push back up to starting position",
                "Keep core tight throughout the movement"
            ]
        },
        {
            "id": 2,
            "name": "Pull-ups",
            "description": "Upper body pulling exercise targeting back and biceps",
            "category": "strength",
            "muscle_groups": ["lats", "rhomboids", "biceps"],
            "equipment": "pull-up bar",
            "difficulty": "intermediate",
            "instructions": [
                "Hang from pull-up bar with overhand grip",
                "Pull your body up until chin clears the bar",
                "Lower yourself with control",
                "Keep shoulders down and back"
            ]
        }
    ]
    
    # Apply filters if provided
    filtered_exercises = sample_exercises
    
    if category:
        filtered_exercises = [ex for ex in filtered_exercises if ex["category"] == category]
    
    if difficulty:
        filtered_exercises = [ex for ex in filtered_exercises if ex["difficulty"] == difficulty]
    
    if muscle_group:
        filtered_exercises = [ex for ex in filtered_exercises if muscle_group in ex["muscle_groups"]]
    
    return filtered_exercises

@router.get("/categories", response_model=List[ExerciseCategory], summary="Get Exercise Categories", description="Retrieve all exercise categories")
async def get_exercise_categories():
    """
    Get all exercise categories
    
    Returns a list of exercise categories with their details
    """
    # TODO: Implement exercise categories retrieval from database
    categories = [
        {
            "id": 1,
            "name": "Strength Training",
            "description": "Exercises focused on building muscle strength and power",
            "exercise_count": 45
        },
        {
            "id": 2,
            "name": "Cardio",
            "description": "Exercises that improve cardiovascular fitness",
            "exercise_count": 30
        },
        {
            "id": 3,
            "name": "Flexibility",
            "description": "Exercises that improve range of motion and flexibility",
            "exercise_count": 25
        },
        {
            "id": 4,
            "name": "HIIT",
            "description": "High-intensity interval training exercises",
            "exercise_count": 20
        }
    ]
    return categories
