"""
Story Analyzer - Level 1 (V2)
故事分析器 - 精简版

职责:
1. 理解故事核心意图
2. 识别角色数量和特征
3. 提取3-5个关键动作 (类型化，不是详细描述)

输出简洁的结构化数据，供后续模板匹配或批量生成使用

Author: Shenzhen Wang & AI
License: MIT
"""
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from backend.llm_client import LLMClient, get_llm_client

logger = logging.getLogger(__name__)


@dataclass
class Character:
    """角色信息"""
    id: str
    name: str
    color: str
    role: str = "character"


@dataclass
class KeyAction:
    """关键动作 (类型化)"""
    type: str  # walk, wave, bow, jump, fight, etc.
    params: Dict[str, Any]  # 动作参数
    intensity: str = "normal"  # slow, normal, fast, intense
    
    def to_dict(self):
        return {
            "type": self.type,
            "params": self.params,
            "intensity": self.intensity
        }


@dataclass
class StoryAnalysis:
    """故事分析结果"""
    story_intent: str
    characters: List[Character]
    key_actions: List[KeyAction]
    duration_estimate: int  # 毫秒
    
    def to_dict(self):
        return {
            "story_intent": self.story_intent,
            "characters": [asdict(c) for c in self.characters],
            "key_actions": [a.to_dict() for a in self.key_actions],
            "duration_estimate": self.duration_estimate
        }


class StoryAnalyzer:
    """故事分析器 - 将自然语言转换为结构化动作序列"""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        初始化分析器
        
        Args:
            llm_client: LLM客户端实例
        """
        self.llm_client = llm_client or get_llm_client()
        self.max_tokens = self.llm_client.get_service_max_tokens('story_planner')
        logger.info(f"Story Analyzer V2 initialized (max_tokens={self.max_tokens})")
    
    def analyze(self, story: str) -> StoryAnalysis:
        """
        分析故事，提取结构化信息
        
        Args:
            story: 用户输入的故事文本
            
        Returns:
            StoryAnalysis 对象
            
        Raises:
            Exception: LLM调用失败或解析失败
        """
        prompt = self._build_prompt(story)
        
        try:
            messages = [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ]
            
            logger.info("Analyzing story with LLM...")
            response = self.llm_client.completion(
                messages=messages,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            
            # 处理可能的markdown包裹
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            logger.info(f"Story analysis complete: {len(result.get('key_actions', []))} actions")
            
            return self._parse_result(result)
            
        except Exception as e:
            logger.error(f"Story analysis failed: {str(e)}")
            raise Exception(f"Failed to analyze story: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """系统提示词"""
        return """你是一位专业的故事分析师。你的任务是将用户的故事描述转换为结构化的动作序列。

🎯 核心任务:
1. 理解故事的核心意图
2. 识别角色数量和特征
3. 提取 3-5 个关键动作 (不要过度细分)
4. 将动作类型化 (使用预定义类型)

📋 支持的动作类型:

基础移动:
- walk: 行走 (params: direction, speed, distance)
  - direction: "left" 向左移动 | "right" 向右移动
  - speed: "slow" | "normal" | "fast"
  - distance: 移动距离(像素)
- run: 跑步
- jump: 跳跃
- turn: 转身

手势动作:
- wave: 挥手 (params: hand, repeat, style)
- point: 指向
- clap: 鼓掌

礼仪动作:
- bow: 鞠躬 (params: depth)
- salute: 敬礼
- handshake: 握手

情感表达:
- celebrate: 庆祝
- think: 思考
- surprise: 惊讶

武术动作:
- punch: 出拳
- kick: 踢腿
- block: 格挡
- dodge: 闪避

复杂动作:
- fight: 打斗 (组合动作)
- dance: 跳舞
- custom: 自定义 (无法用预定义类型描述的)

⚠️ 重要原则:
1. 优先使用预定义类型 (方便使用模板生成)
2. 不要过度细分 (如"走路"不要拆成"抬腿、落地、站稳")
3. 每个动作应该是完整的、有意义的单元
4. 估算合理的总时长

返回 JSON 格式:
{
  "story_intent": "故事的核心意图 (一句话概括)",
  "characters": [
    {
      "id": "char1",
      "name": "角色名",
      "color": "#2196F3",
      "role": "protagonist/antagonist/supporting"
    }
  ],
  "key_actions": [
    {
      "type": "walk",
      "params": {
        "direction": "right",
        "speed": "normal",
        "distance": 200
      },
      "intensity": "normal"
    },
    {
      "type": "wave",
      "params": {
        "hand": "right",
        "repeat": 2,
        "style": "enthusiastic"
      },
      "intensity": "fast"
    }
  ],
  "duration_estimate": 4500
}

示例:

输入: "一个人从左边走进来，热情地挥手打招呼，然后礼貌地鞠躬问好"
输出:
{
  "story_intent": "友好问候",
  "characters": [{"id": "char1", "name": "问候者", "color": "#2196F3", "role": "protagonist"}],
  "key_actions": [
    {"type": "walk", "params": {"direction": "right", "speed": "normal", "distance": 300}, "intensity": "normal"},
    {"type": "wave", "params": {"hand": "both", "repeat": 2, "style": "enthusiastic"}, "intensity": "fast"},
    {"type": "bow", "params": {"depth": "normal"}, "intensity": "slow"}
  ],
  "duration_estimate": 4000
}

注意: "从左边走进来" 意味着从左侧出发向右移动，所以 direction 是 "right"
"""
    
    def _build_prompt(self, story: str) -> str:
        """构建用户提示词"""
        return f"""请分析以下故事并提取结构化信息:

故事:
{story}

要求:
1. 提取 3-5 个关键动作 (不要过度细分)
2. 优先使用预定义动作类型
3. 估算合理的总时长

返回 JSON 格式的分析结果。
"""
    
    def _parse_result(self, result: Dict[str, Any]) -> StoryAnalysis:
        """解析LLM返回结果"""
        # 解析角色
        characters = []
        for c in result.get("characters", []):
            characters.append(Character(
                id=c.get("id", "char1"),
                name=c.get("name", "Character"),
                color=c.get("color", "#2196F3"),
                role=c.get("role", "protagonist")
            ))
        
        # 如果没有角色，创建默认角色
        if not characters:
            characters.append(Character(
                id="char1",
                name="Character",
                color="#2196F3",
                role="protagonist"
            ))
        
        # 解析关键动作
        key_actions = []
        for a in result.get("key_actions", []):
            key_actions.append(KeyAction(
                type=a.get("type", "custom"),
                params=a.get("params", {}),
                intensity=a.get("intensity", "normal")
            ))
        
        # 如果没有动作，创建默认动作
        if not key_actions:
            key_actions.append(KeyAction(
                type="stand",
                params={},
                intensity="normal"
            ))
        
        return StoryAnalysis(
            story_intent=result.get("story_intent", ""),
            characters=characters,
            key_actions=key_actions,
            duration_estimate=result.get("duration_estimate", 3000)
        )
