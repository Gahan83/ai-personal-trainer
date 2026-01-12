"""
AI Service Module

This module provides AI integration using OpenAI's API.
It demonstrates how to interact with AI models for generating content.

Learning Points:
1. How to structure AI services
2. Basic prompt engineering
3. Error handling for AI API calls
4. Response parsing and validation
"""

from openai import OpenAI
from typing import Optional, List, Dict, Any
import json
from app.core.config import settings


class AIService:
    """
    Service for interacting with AI models (OpenAI GPT)
    
    This class demonstrates:
    - Initializing AI clients
    - Making API calls
    - Handling responses
    - Error management
    """
    
    def __init__(self):
        """
        Initialize the AI service with OpenAI client
        
        Note: Make sure OPENAI_API_KEY is set in your .env file
        """
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        
        # Initialize client only if API key is provided
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a completion from the AI model
        
        Args:
            prompt: The user's prompt/question
            system_prompt: System message to set AI behavior (optional)
            max_tokens: Maximum tokens in response
            temperature: Controls randomness (0.0-2.0, higher = more creative)
        
        Returns:
            Generated text response
        
        Learning Points:
        - System prompts set AI behavior
        - User prompts are the actual request
        - Temperature controls creativity vs consistency
        - max_tokens limits response length
        """
        if not self.client:
            raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY in your .env file")
        
        try:
            messages = []
            
            # System prompt sets the AI's role/behavior
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # User prompt is the actual request
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract the generated text
            return response.choices[0].message.content
            
        except Exception as e:
            # Error handling is important for AI services
            raise Exception(f"AI service error: {str(e)}")
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Generate a JSON response from the AI model
        
        This is useful when you need structured data from AI
        
        Args:
            prompt: The user's prompt/question
            system_prompt: System message (optional)
            max_tokens: Maximum tokens in response
        
        Returns:
            Parsed JSON dictionary
        
        Learning Points:
        - AI can generate structured data (JSON)
        - Always parse and validate JSON responses
        - Use system prompts to enforce JSON format
        """
        json_system_prompt = (
            system_prompt or ""
        ) + "\n\nImportant: You must respond with valid JSON only. No additional text."
        
        response_text = await self.generate_completion(
            prompt=prompt,
            system_prompt=json_system_prompt,
            max_tokens=max_tokens,
            temperature=0.3  # Lower temperature for more consistent JSON
        )
        
        try:
            # Parse JSON response
            # Sometimes AI adds markdown formatting, so we strip it
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.startswith("```"):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove trailing ```
            response_text = response_text.strip()
            
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI JSON response: {str(e)}")
    
    async def generate_workout_suggestion(
        self,
        goal: str,
        fitness_level: str,
        duration: int,
        preferences: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a workout suggestion using AI
        
        This demonstrates a practical use case:
        - Taking user inputs
        - Crafting a good prompt
        - Getting structured output
        - Using AI to generate personalized content
        
        Args:
            goal: Fitness goal (e.g., "build muscle", "lose weight")
            fitness_level: User's fitness level (beginner, intermediate, advanced)
            duration: Workout duration in minutes
            preferences: Additional preferences (optional)
        
        Returns:
            Dictionary with workout suggestion
        """
        system_prompt = """You are an expert personal trainer with deep knowledge of fitness, 
exercise science, and workout programming. You create safe, effective, and personalized 
workout plans. Always provide clear, actionable advice."""
        
        user_prompt = f"""Create a personalized workout plan with the following requirements:

- Goal: {goal}
- Fitness Level: {fitness_level}
- Duration: {duration} minutes
{f"- Additional Preferences: {preferences}" if preferences else ""}

Please provide a workout plan in JSON format with this structure:
{{
    "name": "Workout name",
    "description": "Brief description",
    "exercises": [
        {{
            "name": "Exercise name",
            "sets": number of sets,
            "reps": number of reps (or "duration" for time-based exercises),
            "rest": "rest time in seconds",
            "notes": "form tips or variations"
        }}
    ],
    "difficulty": "{fitness_level}",
    "estimated_duration": {duration},
    "tips": ["helpful tip 1", "helpful tip 2"]
}}

Make sure the total workout time is approximately {duration} minutes including rest periods."""
        
        return await self.generate_json(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=1500
        )


# Create a singleton instance
# Note: API calls will fail gracefully if OPENAI_API_KEY is not set
ai_service = AIService()
