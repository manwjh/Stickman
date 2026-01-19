"""
Skeleton Factory
骨骼系统工厂

功能：
1. 统一创建不同DOF的骨骼系统
2. 消除重复的if-else判断
3. 遵循开闭原则：对扩展开放，对修改封闭

Author: Shenzhen Wang & AI
License: MIT
"""
import logging
from typing import Dict, Type, Optional
from backend.models.base_skeleton import BaseSkeleton, SkeletonConfig
from backend.models.skeleton_config_loader import get_skeleton_config

logger = logging.getLogger(__name__)


class SkeletonFactory:
    """骨骼系统工厂（单例模式）"""
    
    _instance = None
    _registry: Dict[str, Type[BaseSkeleton]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, dof_level: str, skeleton_class: Type[BaseSkeleton]):
        """
        注册骨骼系统类
        
        Args:
            dof_level: DOF级别（如'6dof', '12dof'）
            skeleton_class: 骨骼系统类
        """
        cls._registry[dof_level] = skeleton_class
        logger.info(f"Registered skeleton system: {dof_level} -> {skeleton_class.__name__}")
    
    @classmethod
    def create(
        cls,
        dof_level: str,
        config: Optional[SkeletonConfig] = None
    ) -> BaseSkeleton:
        """
        创建骨骼系统实例
        
        Args:
            dof_level: DOF级别
            config: 可选的配置对象，如果不提供则自动加载
            
        Returns:
            BaseSkeleton实例
            
        Raises:
            ValueError: 如果DOF级别不支持
        """
        if dof_level not in cls._registry:
            raise ValueError(
                f"Unsupported DOF level: {dof_level}. "
                f"Available: {list(cls._registry.keys())}"
            )
        
        skeleton_class = cls._registry[dof_level]
        
        # 如果没有提供配置，从配置文件加载
        if config is None:
            config = get_skeleton_config(dof_level)
        
        logger.info(f"Creating {dof_level} skeleton system")
        return skeleton_class(config)
    
    @classmethod
    def get_supported_dof_levels(cls) -> list:
        """
        获取所有支持的DOF级别
        
        Returns:
            DOF级别列表
        """
        return list(cls._registry.keys())
    
    @classmethod
    def is_supported(cls, dof_level: str) -> bool:
        """
        检查是否支持指定的DOF级别
        
        Args:
            dof_level: DOF级别
            
        Returns:
            是否支持
        """
        return dof_level in cls._registry


# 自动注册内置的骨骼系统
def _auto_register():
    """自动注册所有骨骼系统"""
    try:
        from backend.models.skeleton_6dof import Skeleton6DOF
        SkeletonFactory.register('6dof', Skeleton6DOF)
    except ImportError as e:
        logger.warning(f"Failed to register Skeleton6DOF: {e}")
    
    try:
        from backend.models.skeleton_12dof import Skeleton12DOF
        SkeletonFactory.register('12dof', Skeleton12DOF)
    except ImportError as e:
        logger.warning(f"Failed to register Skeleton12DOF: {e}")


# 初始化时自动注册
_auto_register()


# 便捷函数
def create_skeleton(dof_level: str, config: Optional[SkeletonConfig] = None) -> BaseSkeleton:
    """
    创建骨骼系统（便捷函数）
    
    Args:
        dof_level: DOF级别
        config: 可选的配置对象
        
    Returns:
        BaseSkeleton实例
    """
    return SkeletonFactory.create(dof_level, config)
