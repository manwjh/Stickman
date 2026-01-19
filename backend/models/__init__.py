"""
Skeleton Models Package

包含不同自由度的骨骼系统：
- BaseSkeleton: 抽象基类
- 6DOF: 经典简化版（头部位置 + 5个角度）
- 12DOF: 平衡版（12个关键关节）

工厂模式：
- SkeletonFactory: 统一创建骨骼系统
- create_skeleton: 便捷函数

配置管理：
- SkeletonConfig: 配置数据类
- SkeletonConfigLoader: 配置加载器
- get_skeleton_config: 便捷函数

Author: Shenzhen Wang & AI
License: MIT
"""

# 基础类
from .base_skeleton import BaseSkeleton, SkeletonConfig

# 骨骼系统
from .skeleton_6dof import Skeleton6DOF, Pose6DOF
from .skeleton_12dof import Skeleton12DOF, Joint

# 工厂模式
from .skeleton_factory import SkeletonFactory, create_skeleton

# 配置管理
from .skeleton_config_loader import SkeletonConfigLoader, get_skeleton_config

# 其他模型
from .context_memory import ContextMemory
from .scene_plan import ScenePlan, Action, Character, Prop

__all__ = [
    # 基础类
    'BaseSkeleton',
    'SkeletonConfig',
    
    # 骨骼系统
    'Skeleton6DOF',
    'Pose6DOF',
    'Skeleton12DOF',
    'Joint',
    
    # 工厂模式
    'SkeletonFactory',
    'create_skeleton',
    
    # 配置管理
    'SkeletonConfigLoader',
    'get_skeleton_config',
    
    # 其他模型
    'ContextMemory',
    'ScenePlan',
    'Action',
    'Character',
    'Prop'
]
