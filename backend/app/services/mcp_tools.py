"""
MCP (Model Context Protocol) Tools Module

This module demonstrates MCP concepts by creating tool-like structures
that AI can use to interact with your application.

MCP Concepts Demonstrated:
1. Tools: Functions that AI can call
2. Tool Definitions: Metadata about what tools are available
3. Tool Execution: How tools are invoked with parameters
4. Resources: Data sources that tools can access

Learning Points:
- How MCP tools are structured
- Tool definition patterns
- Parameter validation
- Error handling in tools
- Resource access patterns
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import json


# Tool Registry - stores all available tools
# In a real MCP server, this would be managed by the MCP framework
TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_tool(
    name: str,
    description: str,
    parameters: Dict[str, Any],
    handler: Callable
):
    """
    Register a tool in the MCP tool registry
    
    This demonstrates how MCP tools are registered:
    - Each tool has a name, description, and parameters
    - Each tool has a handler function that executes it
    
    Args:
        name: Tool name (must be unique)
        description: What the tool does
        parameters: JSON Schema defining tool parameters
        handler: Function that executes the tool
    """
    TOOL_REGISTRY[name] = {
        "name": name,
        "description": description,
        "parameters": parameters,
        "handler": handler
    }


def get_tool_definition(name: str) -> Optional[Dict[str, Any]]:
    """
    Get tool definition (without handler)
    
    This is what would be sent to the AI to describe available tools
    """
    if name not in TOOL_REGISTRY:
        return None
    
    tool = TOOL_REGISTRY[name].copy()
    # Don't expose the handler function
    tool.pop("handler", None)
    return tool


def list_all_tools() -> List[Dict[str, Any]]:
    """
    List all available tools (for tool discovery)
    
    This is how an MCP server would advertise available tools
    """
    return [
        {
            "name": name,
            "description": tool["description"],
            "parameters": tool["parameters"]
        }
        for name, tool in TOOL_REGISTRY.items()
    ]


def execute_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool with given arguments
    
    This demonstrates how tools are invoked:
    - Tool name identifies which tool to run
    - Arguments are passed to the tool handler
    - Result is returned (or error is raised)
    
    Args:
        name: Tool name
        arguments: Tool arguments (validated against parameters schema)
    
    Returns:
        Tool execution result
    """
    if name not in TOOL_REGISTRY:
        raise ValueError(f"Tool '{name}' not found")
    
    tool = TOOL_REGISTRY[name]
    handler = tool["handler"]
    
    try:
        # Execute the tool handler
        result = handler(**arguments)
        return {
            "success": True,
            "result": result,
            "tool": name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "tool": name
        }


# ============================================================================
# TOOL HANDLERS - These are the actual implementations
# ============================================================================

def _get_user_workout_history(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Tool Handler: Get user's workout history
    
    This simulates accessing a database to get workout history
    In a real application, this would query the database
    """
    # TODO: Replace with actual database query
    return [
        {
            "id": 1,
            "name": "Upper Body Strength",
            "completed_at": "2024-01-15T10:00:00",
            "duration": 45
        },
        {
            "id": 2,
            "name": "Cardio Blast",
            "completed_at": "2024-01-14T10:00:00",
            "duration": 30
        }
    ][:limit]


def _get_exercise_recommendations(
    muscle_group: str,
    difficulty: str = "beginner",
    equipment: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Tool Handler: Get exercise recommendations
    
    This simulates querying an exercise database
    """
    # TODO: Replace with actual database query
    exercises = [
        {
            "id": 1,
            "name": "Push-ups",
            "muscle_groups": ["chest", "shoulders", "triceps"],
            "difficulty": "beginner",
            "equipment": None
        },
        {
            "id": 2,
            "name": "Pull-ups",
            "muscle_groups": ["lats", "biceps"],
            "difficulty": "intermediate",
            "equipment": "pull-up bar"
        }
    ]
    
    # Filter exercises
    filtered = [
        ex for ex in exercises
        if muscle_group in ex["muscle_groups"]
        and ex["difficulty"] == difficulty
        and (equipment is None or ex["equipment"] == equipment)
    ]
    
    return filtered


def _calculate_workout_stats(workout_id: int) -> Dict[str, Any]:
    """
    Tool Handler: Calculate workout statistics
    
    This simulates analyzing workout data
    """
    # TODO: Replace with actual calculation from database
    return {
        "workout_id": workout_id,
        "total_exercises": 5,
        "total_sets": 15,
        "estimated_calories": 250,
        "difficulty_score": 7.5
    }


def _save_workout_progress(
    user_id: int,
    workout_id: int,
    completed_exercises: List[Dict[str, Any]],
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Tool Handler: Save workout progress
    
    This simulates saving data to a database
    """
    # TODO: Replace with actual database save
    return {
        "success": True,
        "progress_id": 123,
        "saved_at": datetime.now().isoformat(),
        "message": "Workout progress saved successfully"
    }


# ============================================================================
# REGISTER TOOLS - Register all available tools
# ============================================================================

# Tool 1: Get User Workout History
register_tool(
    name="get_user_workout_history",
    description="Retrieve a user's workout history. Useful for analyzing past workouts and progress.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "The ID of the user"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of workouts to return",
                "default": 10
            }
        },
        "required": ["user_id"]
    },
    handler=_get_user_workout_history
)

# Tool 2: Get Exercise Recommendations
register_tool(
    name="get_exercise_recommendations",
    description="Get exercise recommendations based on muscle group, difficulty, and equipment availability.",
    parameters={
        "type": "object",
        "properties": {
            "muscle_group": {
                "type": "string",
                "description": "Target muscle group (e.g., 'chest', 'back', 'legs')",
                "enum": ["chest", "back", "legs", "shoulders", "arms", "core"]
            },
            "difficulty": {
                "type": "string",
                "description": "Exercise difficulty level",
                "enum": ["beginner", "intermediate", "advanced"],
                "default": "beginner"
            },
            "equipment": {
                "type": "string",
                "description": "Available equipment (optional)",
                "default": None
            }
        },
        "required": ["muscle_group"]
    },
    handler=_get_exercise_recommendations
)

# Tool 3: Calculate Workout Stats
register_tool(
    name="calculate_workout_stats",
    description="Calculate statistics for a workout (total exercises, sets, estimated calories, etc.).",
    parameters={
        "type": "object",
        "properties": {
            "workout_id": {
                "type": "integer",
                "description": "The ID of the workout"
            }
        },
        "required": ["workout_id"]
    },
    handler=_calculate_workout_stats
)

# Tool 4: Save Workout Progress
register_tool(
    name="save_workout_progress",
    description="Save a user's workout progress including completed exercises and notes.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "The ID of the user"
            },
            "workout_id": {
                "type": "integer",
                "description": "The ID of the workout"
            },
            "completed_exercises": {
                "type": "array",
                "description": "List of completed exercises with details",
                "items": {
                    "type": "object"
                }
            },
            "notes": {
                "type": "string",
                "description": "Optional notes about the workout"
            }
        },
        "required": ["user_id", "workout_id", "completed_exercises"]
    },
    handler=_save_workout_progress
)


# ============================================================================
# UTILITY FUNCTIONS FOR INTEGRATION WITH AI
# ============================================================================

def get_tools_for_ai() -> List[Dict[str, Any]]:
    """
    Get tool definitions formatted for AI consumption
    
    This is how you would provide tool information to an AI assistant
    The AI uses this information to decide which tools to call
    """
    return list_all_tools()


def format_tools_as_prompt() -> str:
    """
    Format tools as a prompt for AI
    
    This demonstrates how tools are described to AI in prompts
    """
    tools_text = "Available Tools:\n\n"
    
    for tool in list_all_tools():
        tools_text += f"Tool: {tool['name']}\n"
        tools_text += f"Description: {tool['description']}\n"
        tools_text += f"Parameters: {json.dumps(tool['parameters'], indent=2)}\n\n"
    
    return tools_text
