"""
Action Template System - 动作模板系统
使用算法生成常见动作，无需LLM调用

优势:
- 生成速度快 (毫秒级)
- 质量稳定
- 物理约束天然满足
- 0 LLM成本

Author: Shenzhen Wang & AI
License: MIT
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import math


@dataclass
class Keyframe:
    """关键帧数据结构"""
    timestamp_ms: int
    description: str
    characters: Dict[str, Dict[str, Any]]
    
    def to_dict(self):
        return {
            "timestamp_ms": self.timestamp_ms,
            "description": self.description,
            "characters": self.characters
        }


class ActionTemplate(ABC):
    """动作模板抽象基类"""
    
    def __init__(self, dof_level: str = "12dof"):
        """
        初始化模板
        
        Args:
            dof_level: 骨骼自由度 (6dof 或 12dof)
        """
        self.dof_level = dof_level
        self.canvas_width = 800
        self.canvas_height = 600
    
    @abstractmethod
    def generate(
        self, 
        character: Dict[str, Any], 
        params: Dict[str, Any]
    ) -> List[Keyframe]:
        """
        生成关键帧
        
        Args:
            character: 角色信息 {"id": "char1", "name": "...", "color": "..."}
            params: 动作参数
            
        Returns:
            关键帧列表
        """
        pass
    
    @abstractmethod
    def get_duration(self, params: Dict[str, Any]) -> int:
        """
        获取动作时长(ms)
        
        Args:
            params: 动作参数
            
        Returns:
            时长(毫秒)
        """
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        验证参数有效性
        
        Args:
            params: 动作参数
            
        Returns:
            是否有效
        """
        return True
    
    def get_standing_pose(self, x: float = 400, y: float = 300) -> Dict[str, Dict[str, float]]:
        """
        获取标准站立姿势 (12DOF)
        
        Args:
            x: 中心X坐标
            y: 中心Y坐标
            
        Returns:
            关节字典
        """
        if self.dof_level == "12dof":
            return {
                "head": {"x": x, "y": y - 60},
                "neck": {"x": x, "y": y - 40},
                "waist": {"x": x, "y": y + 20},
                "left_shoulder": {"x": x - 20, "y": y - 35},
                "left_hand": {"x": x - 50, "y": y + 10},
                "right_shoulder": {"x": x + 20, "y": y - 35},
                "right_hand": {"x": x + 50, "y": y + 10},
                "left_hip": {"x": x - 15, "y": y + 20},
                "left_foot": {"x": x - 15, "y": y + 70},
                "right_hip": {"x": x + 15, "y": y + 20},
                "right_foot": {"x": x + 15, "y": y + 70}
            }
        else:
            # 6DOF implementation
            return {
                "head_x": x,
                "head_y": y - 60,
                "body_angle": 0,
                "left_arm_angle": 0,
                "right_arm_angle": 0,
                "left_leg_angle": 0,
                "right_leg_angle": 0
            }
    
    def lerp(self, a: float, b: float, t: float) -> float:
        """线性插值"""
        return a + (b - a) * t
    
    def ease_in_out(self, t: float) -> float:
        """缓入缓出函数"""
        return t * t * (3 - 2 * t)


class TemplateRegistry:
    """模板注册表"""
    
    def __init__(self):
        self.templates: Dict[str, ActionTemplate] = {}
    
    def register(self, action_type: str, template: ActionTemplate):
        """
        注册模板
        
        Args:
            action_type: 动作类型
            template: 模板实例
        """
        self.templates[action_type] = template
    
    def get(self, action_type: str) -> Optional[ActionTemplate]:
        """
        获取模板
        
        Args:
            action_type: 动作类型
            
        Returns:
            模板实例或None
        """
        return self.templates.get(action_type)
    
    def has(self, action_type: str) -> bool:
        """
        检查是否有该类型的模板
        
        Args:
            action_type: 动作类型
            
        Returns:
            是否存在
        """
        return action_type in self.templates
    
    def list_available(self) -> List[str]:
        """
        列出所有可用的模板类型
        
        Returns:
            类型列表
        """
        return list(self.templates.keys())


# 全局注册表
TEMPLATE_REGISTRY = TemplateRegistry()
