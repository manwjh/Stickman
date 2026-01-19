"""
Skeleton Configuration Loader
骨骼系统配置加载器

功能：
1. 从skeleton_config.yml加载配置
2. 创建SkeletonConfig对象
3. 提供配置缓存

Author: Shenzhen Wang & AI
License: MIT
"""
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from backend.models.base_skeleton import SkeletonConfig

logger = logging.getLogger(__name__)


class SkeletonConfigLoader:
    """骨骼配置加载器（单例模式）"""
    
    _instance = None
    _configs: Dict[str, SkeletonConfig] = {}
    _config_file_path: Optional[Path] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化配置加载器"""
        if not self._config_file_path:
            # 查找配置文件
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent
            self._config_file_path = project_root / "skeleton_config.yml"
            
            if not self._config_file_path.exists():
                logger.warning(f"Skeleton config file not found: {self._config_file_path}")
    
    def load_config(self, dof_level: str) -> SkeletonConfig:
        """
        加载指定DOF级别的配置
        
        Args:
            dof_level: DOF级别（'6dof', '12dof'等）
            
        Returns:
            SkeletonConfig对象
        """
        # 检查缓存
        if dof_level in self._configs:
            return self._configs[dof_level]
        
        # 从文件加载
        config = self._load_from_file(dof_level)
        
        # 缓存配置
        self._configs[dof_level] = config
        
        logger.info(f"Loaded config for {dof_level}: {config.joint_count} joints")
        
        return config
    
    def _load_from_file(self, dof_level: str) -> SkeletonConfig:
        """从YAML文件加载配置"""
        if not self._config_file_path or not self._config_file_path.exists():
            # 返回默认配置
            return self._get_default_config(dof_level)
        
        try:
            with open(self._config_file_path, 'r', encoding='utf-8') as f:
                all_configs = yaml.safe_load(f)
            
            config_key = f"skeleton_{dof_level}"
            if config_key not in all_configs:
                logger.warning(f"Config key '{config_key}' not found, using defaults")
                return self._get_default_config(dof_level)
            
            raw_config = all_configs[config_key]
            
            return SkeletonConfig(
                dof_level=dof_level,
                joint_count=raw_config.get('joint_count', 0),
                canvas_width=800,
                canvas_height=600,
                bone_lengths=raw_config.get('bone_lengths', raw_config.get('proportions', {})),
                angle_limits=raw_config.get('angle_limits', {}),
                tolerance=raw_config.get('tolerance', {})
            )
            
        except Exception as e:
            logger.error(f"Failed to load config from file: {e}")
            return self._get_default_config(dof_level)
    
    def _get_default_config(self, dof_level: str) -> SkeletonConfig:
        """获取默认配置"""
        defaults = {
            '6dof': SkeletonConfig(
                dof_level='6dof',
                joint_count=6,
                bone_lengths={
                    'head_radius': 20,
                    'body_length': 60,
                    'arm_length': 40,
                    'leg_length': 50
                },
                angle_limits={
                    'body_angle': (-45, 45),
                    'arm_angle': (-180, 180),
                    'leg_angle': (-45, 45)
                }
            ),
            '12dof': SkeletonConfig(
                dof_level='12dof',
                joint_count=12,
                bone_lengths={
                    'head_radius': 20,
                    'neck_to_head': 20,
                    'neck_to_waist': 60,
                    'shoulder_width': 40,
                    'arm_length': 50,
                    'hip_width': 30,
                    'leg_length': 50
                },
                tolerance={
                    'head_radius': 0.3,
                    'neck_to_head': 0.3,
                    'neck_to_waist': 0.3,
                    'shoulder_width': 0.4,
                    'arm_length': 0.5,
                    'hip_width': 0.4,
                    'leg_length': 0.6
                }
            )
        }
        
        if dof_level in defaults:
            return defaults[dof_level]
        else:
            raise ValueError(f"Unsupported DOF level: {dof_level}")
    
    def clear_cache(self):
        """清空配置缓存"""
        self._configs.clear()
        logger.info("Skeleton config cache cleared")


# 全局单例实例
_config_loader = SkeletonConfigLoader()


def get_skeleton_config(dof_level: str) -> SkeletonConfig:
    """
    获取骨骼配置（便捷函数）
    
    Args:
        dof_level: DOF级别
        
    Returns:
        SkeletonConfig对象
    """
    return _config_loader.load_config(dof_level)
