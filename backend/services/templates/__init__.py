"""
模板初始化
"""
from .template_engine import TEMPLATE_REGISTRY
from .actions.walk import WalkTemplate
from .actions.wave import WaveTemplate
from .actions.bow import BowTemplate

# 注册所有模板
def register_all_templates(dof_level: str = "12dof"):
    """注册所有预定义模板"""
    TEMPLATE_REGISTRY.register("walk", WalkTemplate(dof_level))
    TEMPLATE_REGISTRY.register("wave", WaveTemplate(dof_level))
    TEMPLATE_REGISTRY.register("bow", BowTemplate(dof_level))

__all__ = [
    "TEMPLATE_REGISTRY",
    "register_all_templates"
]
