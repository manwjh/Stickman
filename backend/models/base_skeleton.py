"""
Base Skeleton System
骨骼系统抽象基类

遵循SOLID原则：
- Single Responsibility: 定义骨骼系统的统一接口
- Open/Closed: 对扩展开放，对修改封闭
- Liskov Substitution: 所有子类可以替换基类
- Interface Segregation: 提供最小必要接口
- Dependency Inversion: 依赖抽象而非具体实现

Author: Shenzhen Wang & AI
License: MIT
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union
from dataclasses import dataclass


@dataclass
class SkeletonConfig:
    """骨骼系统配置"""
    dof_level: str
    joint_count: int
    canvas_width: int = 800
    canvas_height: int = 600
    bone_lengths: Dict[str, float] = None
    angle_limits: Dict[str, tuple] = None
    tolerance: Dict[str, float] = None
    
    def __post_init__(self):
        if self.bone_lengths is None:
            self.bone_lengths = {}
        if self.angle_limits is None:
            self.angle_limits = {}
        if self.tolerance is None:
            self.tolerance = {}


class BaseSkeleton(ABC):
    """骨骼系统抽象基类"""
    
    def __init__(self, config: SkeletonConfig):
        """
        初始化骨骼系统
        
        Args:
            config: 骨骼系统配置
        """
        self.config = config
        self.dof_level = config.dof_level
        self.joint_count = config.joint_count
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        获取LLM系统提示词
        
        Returns:
            系统提示词字符串
        """
        pass
    
    @abstractmethod
    def validate(self, data: Union[Dict[str, Any], Any]) -> List[str]:
        """
        验证姿态数据的有效性
        
        Args:
            data: 姿态数据（可以是pose、joints等）
            
        Returns:
            错误列表，空列表表示验证通过
        """
        pass
    
    @abstractmethod
    def get_default_pose(self) -> Dict[str, Any]:
        """
        获取默认姿态
        
        Returns:
            默认姿态数据
        """
        pass
    
    @abstractmethod
    def get_data_field_name(self) -> str:
        """
        获取数据字段名称（如'pose'、'joints'）
        
        Returns:
            字段名称
        """
        pass
    
    def get_joint_count(self) -> int:
        """
        获取关节数量
        
        Returns:
            关节数量
        """
        return self.joint_count
    
    def get_dof_level(self) -> str:
        """
        获取自由度级别
        
        Returns:
            DOF级别字符串
        """
        return self.dof_level
    
    def validate_canvas_bounds(
        self,
        x: float,
        y: float,
        joint_name: str = ""
    ) -> List[str]:
        """
        验证坐标是否在画布范围内
        
        Args:
            x: X坐标
            y: Y坐标
            joint_name: 关节名称（用于错误信息）
            
        Returns:
            错误列表
        """
        errors = []
        margin = 50  # 允许边界外50px的容差
        
        if not (-margin <= x <= self.config.canvas_width + margin):
            errors.append(
                f"{joint_name} 的 x 坐标超出画布: {x:.1f} "
                f"(范围: {-margin} ~ {self.config.canvas_width + margin})"
            )
        
        if not (-margin <= y <= self.config.canvas_height + margin):
            errors.append(
                f"{joint_name} 的 y 坐标超出画布: {y:.1f} "
                f"(范围: {-margin} ~ {self.config.canvas_height + margin})"
            )
        
        return errors
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"{self.__class__.__name__}(dof={self.dof_level}, joints={self.joint_count})"
