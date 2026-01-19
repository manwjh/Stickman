"""
Animation Generator - Level 2 (V2)
动画生成器 - 智能生成模式

两种生成模式:
1. 模板生成 (优先): 使用算法，0次LLM调用
2. LLM批量生成 (备用): 一次生成所有关键帧

Author: Shenzhen Wang & AI
License: MIT
"""
import json
import logging
from typing import Dict, Any, List, Optional
from backend.llm_client import LLMClient, get_llm_client
from backend.models.base_skeleton import BaseSkeleton
from backend.models.skeleton_factory import create_skeleton
from .story_analyzer import StoryAnalysis, KeyAction, Character
from .templates import TEMPLATE_REGISTRY, register_all_templates

logger = logging.getLogger(__name__)


class AnimationGenerator:
    """动画生成器 - 智能选择生成模式"""
    
    def __init__(
        self, 
        dof_level: str = "12dof",
        llm_client: Optional[LLMClient] = None
    ):
        """
        初始化生成器
        
        Args:
            dof_level: 骨骼自由度 (6dof 或 12dof)
            llm_client: LLM客户端实例
        """
        self.dof_level = dof_level
        self.llm_client = llm_client or get_llm_client()
        self.max_tokens = self.llm_client.get_service_max_tokens('animator')
        self.skeleton = create_skeleton(dof_level)
        
        # 注册所有模板
        register_all_templates(dof_level)
        
        logger.info(
            f"Animation Generator V2 initialized "
            f"(dof={dof_level}, templates={len(TEMPLATE_REGISTRY.list_available())})"
        )
    
    def generate(self, story_analysis: StoryAnalysis) -> Dict[str, Any]:
        """
        生成动画数据
        
        Args:
            story_analysis: 故事分析结果
            
        Returns:
            动画数据字典
        """
        key_actions = story_analysis.key_actions
        characters = story_analysis.characters
        
        # 检查是否所有动作都有模板
        all_have_templates = all(
            TEMPLATE_REGISTRY.has(action.type) 
            for action in key_actions
        )
        
        if all_have_templates:
            logger.info("所有动作都有模板，使用模板生成 (0次LLM调用)")
            return self._generate_with_templates(story_analysis)
        else:
            logger.info("部分动作无模板，使用LLM批量生成 (1次LLM调用)")
            return self._generate_with_llm(story_analysis)
    
    def _generate_with_templates(self, story_analysis: StoryAnalysis) -> Dict[str, Any]:
        """
        使用模板生成所有关键帧 (算法生成，0次LLM调用)
        
        Args:
            story_analysis: 故事分析结果
            
        Returns:
            动画数据
        """
        keyframes = []
        current_time = 0
        
        for action in story_analysis.key_actions:
            template = TEMPLATE_REGISTRY.get(action.type)
            
            if template is None:
                logger.warning(f"No template for action type: {action.type}")
                continue
            
            # 使用第一个角色
            character = story_analysis.characters[0]
            character_dict = {
                "id": character.id,
                "name": character.name,
                "color": character.color
            }
            
            # 生成关键帧
            action_keyframes = template.generate(character_dict, action.params)
            
            # 获取动作时长（用于计算下一个动作的起始时间）
            action_duration = template.get_duration(action.params)
            
            # 调整时间戳并添加关键帧
            for kf in action_keyframes:
                kf.timestamp_ms += current_time
                keyframes.append(kf.to_dict())
            
            # 更新当前时间：使用最后一个关键帧的时间戳 + 50ms缓冲
            # 这样下一个动作会在这个动作的最后一帧之后开始，避免时间戳重复
            if action_keyframes:
                last_kf_time = action_keyframes[-1].timestamp_ms
                current_time = last_kf_time + 50  # 50ms缓冲避免重复
            else:
                current_time += action_duration
        
        # 构建动画数据
        return {
            "characters": [
                {
                    "id": c.id,
                    "name": c.name,
                    "color": c.color,
                    "role": c.role
                }
                for c in story_analysis.characters
            ],
            "keyframes": keyframes,
            "dof_level": self.dof_level,
            "generation_method": "template"
        }
    
    def _generate_with_llm(self, story_analysis: StoryAnalysis) -> Dict[str, Any]:
        """
        使用LLM批量生成所有关键帧 (1次LLM调用)
        
        Args:
            story_analysis: 故事分析结果
            
        Returns:
            动画数据
        """
        prompt = self._build_batch_prompt(story_analysis)
        
        try:
            messages = [
                {"role": "system", "content": self.skeleton.get_system_prompt()},
                {"role": "user", "content": prompt}
            ]
            
            logger.info("Calling LLM for batch generation...")
            response = self.llm_client.completion(
                messages=messages,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            
            # 处理markdown包裹
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            
            # 确保有keyframes字段
            if "keyframes" not in result:
                raise ValueError("LLM响应缺少keyframes字段")
            
            keyframes = result["keyframes"]
            logger.info(f"LLM批量生成成功: {len(keyframes)}个关键帧")
            
            return {
                "characters": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "color": c.color,
                        "role": c.role
                    }
                    for c in story_analysis.characters
                ],
                "keyframes": keyframes,
                "dof_level": self.dof_level,
                "generation_method": "llm_batch"
            }
            
        except Exception as e:
            logger.error(f"LLM批量生成失败: {str(e)}")
            raise Exception(f"Failed to generate animation: {str(e)}")
    
    def _build_batch_prompt(self, story_analysis: StoryAnalysis) -> str:
        """
        构建批量生成的prompt
        
        Args:
            story_analysis: 故事分析结果
            
        Returns:
            prompt字符串
        """
        # 构建动作描述
        actions_desc = []
        for i, action in enumerate(story_analysis.key_actions, 1):
            params_str = ", ".join([f"{k}={v}" for k, v in action.params.items()])
            actions_desc.append(
                f"{i}. {action.type} ({params_str}) - 强度: {action.intensity}"
            )
        
        prompt = f"""请为以下动作序列生成完整的动画关键帧。

**故事意图**: {story_analysis.story_intent}

**角色**:
{story_analysis.characters[0].name} (ID: {story_analysis.characters[0].id})

**动作序列**:
{chr(10).join(actions_desc)}

**总时长估计**: {story_analysis.duration_estimate}ms

**要求**:
1. **一次性生成所有关键帧** (不要逐帧生成)
2. 每个动作生成 2-3 个关键帧 (起始、关键时刻、结束)
3. 确保关键帧之间动作连贯流畅
4. 严格遵守骨骼约束
5. timestamp_ms 必须严格递增
6. 返回格式: {{"keyframes": [...]}}

现在请生成所有关键帧:
"""
        return prompt
