"""
Walk Template - 行走动作模板
使用数学计算生成自然的行走动画

Author: Shenzhen Wang & AI
License: MIT
"""
import math
from typing import Dict, Any, List
from ..template_engine import ActionTemplate, Keyframe


class WalkTemplate(ActionTemplate):
    """行走动作模板"""
    
    def generate(
        self, 
        character: Dict[str, Any], 
        params: Dict[str, Any]
    ) -> List[Keyframe]:
        """
        生成行走动画
        
        参数:
            direction: "left" | "right" - 行走方向 (向左移动 | 向右移动)
            speed: "slow" | "normal" | "fast" - 行走速度
            distance: 行走距离 (像素)
        """
        direction = params.get("direction", "right")
        speed = params.get("speed", "normal")
        distance = params.get("distance", 200)
        
        char_id = character["id"]
        
        # 根据方向确定起点和终点
        if direction == "left":
            start_x = 700
            end_x = start_x - distance
        else:
            start_x = 100
            end_x = start_x + distance
        
        center_y = 300
        
        # 根据速度确定时长和步数
        speed_multipliers = {"slow": 1.5, "normal": 1.0, "fast": 0.7}
        base_duration = 1200  # 基础时长
        duration = int(base_duration * speed_multipliers.get(speed, 1.0))
        
        # 生成更多关键帧以确保平滑动画
        # 每200ms一个关键帧 (约5fps)，让GSAP负责进一步插值
        frame_interval = 200  # ms
        num_frames = max(duration // frame_interval + 1, 3)  # 至少3帧
        
        keyframes = []
        for i in range(num_frames):
            t = i / (num_frames - 1) if num_frames > 1 else 0
            timestamp = int(duration * t)
            x = self.lerp(start_x, end_x, t)
            
            # 计算行走相位 (用于腿部和手臂摆动)
            phase = t * 2.0  # 2个完整步伐
            
            joints = self._create_walk_pose(x, center_y, phase)
            
            keyframes.append(Keyframe(
                timestamp_ms=timestamp,
                description=self._get_description(i, num_frames, direction),
                characters={
                    char_id: {"joints": joints}
                }
            ))
        
        return keyframes
    
    def _create_walk_pose(self, x: float, y: float, phase: float) -> Dict[str, Dict[str, float]]:
        """
        创建行走姿势
        
        Args:
            x: 中心X坐标
            y: 中心Y坐标
            phase: 步伐相位 (0-2)
        """
        # 腿部摆动 (正弦波)
        leg_swing = math.sin(phase * math.pi) * 20
        # 手臂摆动 (反相)
        arm_swing = math.sin(phase * math.pi + math.pi) * 15
        # 身体轻微上下运动
        body_bounce = abs(math.sin(phase * math.pi)) * 5
        
        return {
            "head": {"x": x, "y": y - 60 - body_bounce},
            "neck": {"x": x, "y": y - 40 - body_bounce},
            "waist": {"x": x, "y": y + 20 - body_bounce},
            "left_shoulder": {"x": x - 20, "y": y - 35 - body_bounce},
            "left_hand": {"x": x - 35 + arm_swing, "y": y + 10 - body_bounce},
            "right_shoulder": {"x": x + 20, "y": y - 35 - body_bounce},
            "right_hand": {"x": x + 35 - arm_swing, "y": y + 10 - body_bounce},
            "left_hip": {"x": x - 15, "y": y + 20 - body_bounce},
            "left_foot": {"x": x - 15 - leg_swing, "y": y + 70},
            "right_hip": {"x": x + 15, "y": y + 20 - body_bounce},
            "right_foot": {"x": x + 15 + leg_swing, "y": y + 70}
        }
    
    def _get_description(self, index: int, total: int, direction: str) -> str:
        """获取关键帧描述"""
        if index == 0:
            return f"开始从{'左侧' if direction == 'left' else '右侧'}行走"
        elif index == total - 1:
            return "行走结束，站稳"
        else:
            return f"行走中 (步{index}/{total-1})"
    
    def get_duration(self, params: Dict[str, Any]) -> int:
        """获取动作时长"""
        speed = params.get("speed", "normal")
        speed_multipliers = {"slow": 1.5, "normal": 1.0, "fast": 0.7}
        return int(1200 * speed_multipliers.get(speed, 1.0))
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数"""
        direction = params.get("direction", "right")
        speed = params.get("speed", "normal")
        
        if direction not in ["left", "right"]:
            return False
        if speed not in ["slow", "normal", "fast"]:
            return False
        
        return True
