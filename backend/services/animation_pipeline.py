"""
Animation Pipeline - 3级流水线
新一代动画生成系统

架构:
Level 1: Story Analyzer - 故事分析 (1次LLM)
Level 2: Animation Generator - 动画生成 (模板:0次 或 LLM:1次)
Level 3: Animation Optimizer - 动画优化 (0次LLM)

Author: Shenzhen Wang & AI
License: MIT
"""
import time
import logging
from typing import Dict, Any, Optional
from .story_analyzer import StoryAnalyzer
from .animation_generator import AnimationGenerator
from .animation_optimizer import AnimationOptimizer
from backend.utils.debug_logger import get_debug_logger

logger = logging.getLogger(__name__)


class AnimationPipelineV2:
    """3级流水线 - 新一代动画生成系统"""
    
    def __init__(self, dof_level: str = "12dof", enable_optimization: bool = True):
        self.dof_level = dof_level
        self.enable_optimization = enable_optimization
        
        logger.info(f"Initializing Animation Pipeline (dof={dof_level})")
        
        self.story_analyzer = StoryAnalyzer()
        self.animation_generator = AnimationGenerator(dof_level=dof_level)
        self.animation_optimizer = AnimationOptimizer(dof_level=dof_level)
        
        self.debug_logger = get_debug_logger()
        
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "avg_time_ms": 0,
            "total_time_ms": 0,
            "llm_calls_total": 0,
            "template_generations": 0,
            "llm_generations": 0
        }
        
        logger.info("Animation Pipeline initialized successfully")
    
    def generate(self, story: str) -> Dict[str, Any]:
        """完整的动画生成流程"""
        start_time = time.time()
        self.stats["total_requests"] += 1
        
        session_id = self.debug_logger.start_session(story, self.dof_level)
        
        llm_calls = 0
        
        try:
            logger.info(f"Starting animation generation (length: {len(story)})")
            
            logger.info("Level 1: Story Analysis...")
            story_analysis = self.story_analyzer.analyze(story)
            llm_calls += 1
            
            self.debug_logger.log_custom(
                "01_story_analysis.json",
                story_analysis.to_dict()
            )
            
            logger.info(
                f"Story analyzed: {len(story_analysis.characters)} characters, "
                f"{len(story_analysis.key_actions)} key actions"
            )
            
            logger.info("Level 2: Animation Generation...")
            animation_data = self.animation_generator.generate(story_analysis)
            
            if animation_data.get("generation_method") == "llm_batch":
                llm_calls += 1
                self.stats["llm_generations"] += 1
            else:
                self.stats["template_generations"] += 1
            
            self.debug_logger.log_custom(
                "02_animation_raw.json",
                animation_data
            )
            
            # 生成关键帧SVG可视化
            self.debug_logger._generate_keyframe_svgs(animation_data)
            
            logger.info(
                f"Generated {len(animation_data.get('keyframes', []))} keyframes "
                f"(method: {animation_data.get('generation_method')})"
            )
            
            if self.enable_optimization:
                logger.info("Level 3: Animation Optimization...")
                animation_data = self.animation_optimizer.optimize(
                    animation_data,
                    auto_fix=True,
                    interpolate=True,  # 开启后端插值，生成所有帧
                    target_fps=30  # 30fps足够流畅，避免数据过大
                )
                
                self.debug_logger.log_custom(
                    "03_animation_optimized.json",
                    animation_data
                )
                
                # 生成插值后所有帧的SVG
                self.debug_logger._generate_keyframe_svgs(animation_data)
                
                logger.info(
                    f"Optimized to {len(animation_data.get('keyframes', []))} frames"
                )
            
            elapsed_ms = (time.time() - start_time) * 1000
            self.stats["successful"] += 1
            self.stats["total_time_ms"] += elapsed_ms
            self.stats["avg_time_ms"] = self.stats["total_time_ms"] / self.stats["successful"]
            self.stats["llm_calls_total"] += llm_calls
            
            logger.info(
                f"Generation complete in {elapsed_ms:.0f}ms "
                f"({llm_calls} LLM calls)"
            )
            
            # 将 debug_session_id 添加到动画数据中
            animation_data["debug_session_id"] = session_id
            
            result = {
                "success": True,
                "data": animation_data,
                "metadata": {
                    "dof_level": self.dof_level,
                    "generation_time_ms": elapsed_ms,
                    "keyframes_generated": len(animation_data.get("keyframes", [])),
                    "llm_calls": llm_calls,
                    "generation_method": animation_data.get("generation_method"),
                    "optimization_enabled": self.enable_optimization,
                    "story_analysis": story_analysis.to_dict(),
                    "debug_session_id": session_id
                }
            }
            
            self.debug_logger.log_final_output(animation_data, result["metadata"])
            self.debug_logger.end_session()
            
            return result
            
        except Exception as e:
            self.stats["failed"] += 1
            elapsed_ms = (time.time() - start_time) * 1000
            
            logger.error(f"Animation generation failed: {str(e)}", exc_info=True)
            
            self.debug_logger.log_error(e, "Animation Generation")
            self.debug_logger.end_session()
            
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "dof_level": self.dof_level,
                    "generation_time_ms": elapsed_ms,
                    "llm_calls": llm_calls,
                    "debug_session_id": session_id
                }
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取流水线统计数据"""
        stats = self.stats.copy()
        
        if stats["total_requests"] > 0:
            stats["avg_llm_calls"] = stats["llm_calls_total"] / stats["total_requests"]
        else:
            stats["avg_llm_calls"] = 0
        
        return stats
    
    def reset_stats(self):
        """重置统计数据"""
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "avg_time_ms": 0,
            "total_time_ms": 0,
            "llm_calls_total": 0,
            "template_generations": 0,
            "llm_generations": 0
        }
        logger.info("Pipeline stats reset")
