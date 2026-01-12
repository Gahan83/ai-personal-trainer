"""
MCP Tools API Endpoint

This endpoint demonstrates MCP concepts by exposing tools via REST API.
This helps you understand how MCP tools work in practice.

Learning Points:
- How to expose tools via API
- Tool discovery
- Tool execution
- Error handling
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.mcp_tools import (
    list_all_tools,
    execute_tool,
    get_tool_definition,
    format_tools_as_prompt
)

router = APIRouter(prefix="/mcp", tags=["mcp"])


class ToolExecutionRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]


@router.get("/tools", summary="List All Tools", description="Get a list of all available MCP tools")
async def list_tools():
    """
    List all available MCP tools
    
    This endpoint demonstrates tool discovery:
    - Shows what tools are available
    - Displays tool descriptions
    - Shows tool parameters
    
    Returns:
        List of tool definitions
    """
    tools = list_all_tools()
    return {
        "success": True,
        "tools": tools,
        "count": len(tools)
    }


@router.get("/tools/{tool_name}", summary="Get Tool Definition", description="Get the definition of a specific tool")
async def get_tool(tool_name: str):
    """
    Get the definition of a specific tool
    
    - **tool_name**: Name of the tool to retrieve
    
    Returns:
        Tool definition with parameters
    """
    tool = get_tool_definition(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    return {
        "success": True,
        "tool": tool
    }


@router.post("/tools/execute", summary="Execute Tool", description="Execute an MCP tool with arguments")
async def execute_mcp_tool(request: ToolExecutionRequest):
    """
    Execute an MCP tool with given arguments
    
    This demonstrates how tools are invoked:
    - Tool name identifies which tool to run
    - Arguments are passed to the tool
    - Result or error is returned
    
    - **tool_name**: Name of the tool to execute
    - **arguments**: Tool arguments (must match tool parameters)
    
    Example request:
    {
        "tool_name": "get_exercise_recommendations",
        "arguments": {
            "muscle_group": "chest",
            "difficulty": "beginner"
        }
    }
    
    Returns:
        Tool execution result
    """
    try:
        result = execute_tool(request.tool_name, request.arguments)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool execution error: {str(e)}")


@router.get("/tools/prompt", summary="Get Tools as Prompt", description="Get tool descriptions formatted as a prompt for AI")
async def get_tools_prompt():
    """
    Get tool descriptions formatted as a prompt
    
    This shows how tools are described to AI:
    - Tool names and descriptions
    - Parameter definitions
    - Usage examples
    
    Returns:
        Formatted text describing all tools
    """
    prompt = format_tools_as_prompt()
    return {
        "success": True,
        "prompt": prompt
    }
