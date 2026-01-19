"""
Scene Plan Data Models
场景规划数据模型

定义故事规划器的输出数据结构

Author: Shenzhen Wang & AI
License: MIT
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Character:
    """角色定义"""
    id: str
    name: str
    role: str = "character"
    color: str = "#2196F3"
    description: str = ""


@dataclass
class Prop:
    """道具定义"""
    id: str
    type: str  # "weapon", "object", "background"
    name: str
    description: str = ""


@dataclass
class Action:
    """动作定义"""
    action_id: str
    description: str
    duration_ms: int
    character_ids: List[str]
    tags: List[str] = field(default_factory=list)  # "jump", "attack", "walk"
    intensity: str = "normal"  # "slow", "normal", "fast", "intense"


@dataclass
class ScenePlan:
    """场景规划"""
    story_summary: str
    characters: List[Character]
    props: List[Prop]
    actions: List[Action]
    setting: Dict[str, Any] = field(default_factory=dict)  # location, mood, style
    total_duration_ms: int = 0
    
    def __post_init__(self):
        """计算总时长"""
        if self.total_duration_ms == 0:
            self.total_duration_ms = sum(action.duration_ms for action in self.actions)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "story_summary": self.story_summary,
            "characters": [
                {
                    "id": c.id,
                    "name": c.name,
                    "role": c.role,
                    "color": c.color,
                    "description": c.description
                }
                for c in self.characters
            ],
            "props": [
                {
                    "id": p.id,
                    "type": p.type,
                    "name": p.name,
                    "description": p.description
                }
                for p in self.props
            ],
            "actions": [
                {
                    "action_id": a.action_id,
                    "description": a.description,
                    "duration_ms": a.duration_ms,
                    "character_ids": a.character_ids,
                    "tags": a.tags,
                    "intensity": a.intensity
                }
                for a in self.actions
            ],
            "setting": self.setting,
            "total_duration_ms": self.total_duration_ms
        }
