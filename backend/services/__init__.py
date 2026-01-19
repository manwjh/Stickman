"""
V2 架构 - 新一代动画生成系统
3级流水线: Story Analyzer → Animation Generator → Animation Optimizer

优势:
- LLM调用次数: 17次 → 2-3次
- 生成时间: 167秒 → 20-30秒
- 成本: 降低 80%

Author: Shenzhen Wang & AI
License: MIT
"""

__version__ = "2.0.0"
__all__ = [
    "StoryAnalyzer",
    "AnimationGenerator", 
    "AnimationOptimizer",
    "AnimationPipelineV2"
]
