"""
Animation Data Validator

Uses Pydantic to validate LLM-generated animation data:
- Data structure integrity
- Coordinate range checking
- Type safety validation

Author: Shenzhen Wang & AI
License: MIT
"""
from typing import Dict, Any, List
from pydantic import BaseModel, Field, validator


class Point(BaseModel):
    """2D Point"""
    cx: float = Field(..., ge=0, le=800)
    cy: float = Field(..., ge=0, le=600)
    r: float = Field(20, ge=15, le=30)


class Line(BaseModel):
    """Line segment"""
    x1: float = Field(..., ge=0, le=800)
    y1: float = Field(..., ge=0, le=600)
    x2: float = Field(..., ge=0, le=800)
    y2: float = Field(..., ge=0, le=600)


class StickFigure(BaseModel):
    """Stick figure pose"""
    head: Point
    body: Line
    left_arm: Line
    right_arm: Line
    left_leg: Line
    right_leg: Line


class Frame(BaseModel):
    """Animation frame"""
    timestamp: int = Field(..., ge=0)
    characters: Dict[str, StickFigure]
    text: str = ""


class Scene(BaseModel):
    """Animation scene"""
    id: str
    duration: int = Field(..., gt=0)
    description: str = ""
    frames: List[Frame] = Field(..., min_items=1)


class Character(BaseModel):
    """Character definition"""
    id: str
    name: str = ""
    color: str = "#2196F3"


class Canvas(BaseModel):
    """Canvas settings"""
    width: int = 800
    height: int = 600


class AnimationData(BaseModel):
    """Complete animation data"""
    title: str = "AI Generated Animation"
    description: str = ""
    canvas: Canvas = Canvas()
    characters: List[Character] = Field(..., min_items=1)
    scenes: List[Scene] = Field(..., min_items=1)


def validate_animation_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize animation data
    
    Args:
        data: Raw animation data from LLM
        
    Returns:
        Validated animation data
        
    Raises:
        ValueError: If data is invalid
    """
    try:
        # Validate using Pydantic model
        animation = AnimationData(**data)
        return animation.model_dump()
    
    except Exception as e:
        raise ValueError(f"Invalid animation data: {str(e)}")


def add_intermediate_frames(data: Dict[str, Any], fps: int = 30) -> Dict[str, Any]:
    """
    Add intermediate frames for smoother animation
    (Optional enhancement - can be implemented later)
    
    Args:
        data: Animation data
        fps: Target frames per second
        
    Returns:
        Animation data with interpolated frames
    """
    # TODO: Implement frame interpolation
    return data
