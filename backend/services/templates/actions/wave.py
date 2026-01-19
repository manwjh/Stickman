"""
Wave Template - 挥手动作模板
生成自然的挥手问候动画

Author: Shenzhen Wang & AI
License: MIT
"""
import math
from typing import Dict, Any, List
from ..template_engine import ActionTemplate, Keyframe


class WaveTemplate(ActionTemplate):
    """挥手动作模板"""
    
    def generate(
        self, 
        character: Dict[str, Any], 
        params: Dict[str, Any]
    ) -> List[Keyframe]:
        """
        生成挥手动画
        
        参数:
            hand: "left" | "right" | "both" - 挥手的手
            repeat: 挥手次数 (1-3)
            style: "normal" | "enthusiastic" - 挥手风格
        """
        hand = params.get("hand", "right")
        repeat = params.get("repeat", 1)
        style = params.get("style", "normal")
        
        char_id = character["id"]
        x, y = 400, 300  # 画布中心
        
        # 根据风格确定幅度和速度
        if style == "enthusiastic":
            amplitude = 60
            duration_per_wave = 500
        else:
            amplitude = 40
            duration_per_wave = 700
        
        total_duration = duration_per_wave * repeat
        
        keyframes = []
        
        # 起始姿势
        keyframes.append(Keyframe(
            timestamp_ms=0,
            description="准备挥手",
            characters={
                char_id: {"joints": self.get_standing_pose(x, y)}
            }
        ))
        
        # 每次挥手生成更多中间帧以确保平滑
        for i in range(repeat):
            wave_start_time = i * duration_per_wave
            wave_end_time = (i + 1) * duration_per_wave
            
            # 每次挥手分4个阶段：准备→上升→高点→下降
            # 上升阶段 (0.3)
            t_rise = wave_start_time + duration_per_wave * 0.3
            joints_rise = self._create_wave_pose(
                x, y, hand, amplitude * 0.5, phase="rising"
            )
            keyframes.append(Keyframe(
                timestamp_ms=int(t_rise),
                description=f"挥手第{i+1}次 - 上升",
                characters={
                    char_id: {"joints": joints_rise}
                }
            ))
            
            # 高点 (0.5)
            t_peak = wave_start_time + duration_per_wave * 0.5
            joints_peak = self._create_wave_pose(
                x, y, hand, amplitude, phase="peak"
            )
            keyframes.append(Keyframe(
                timestamp_ms=int(t_peak),
                description=f"挥手第{i+1}次 - 高点",
                characters={
                    char_id: {"joints": joints_peak}
                }
            ))
            
            # 下降阶段 (0.7)
            if i < repeat - 1:  # 最后一次不需要中间下降帧
                t_fall = wave_start_time + duration_per_wave * 0.7
                joints_fall = self._create_wave_pose(
                    x, y, hand, amplitude * 0.5, phase="falling"
                )
                keyframes.append(Keyframe(
                    timestamp_ms=int(t_fall),
                    description=f"挥手第{i+1}次 - 下降",
                    characters={
                        char_id: {"joints": joints_fall}
                    }
                ))
        
        # 结束姿势
        keyframes.append(Keyframe(
            timestamp_ms=total_duration,
            description="挥手结束",
            characters={
                char_id: {"joints": self.get_standing_pose(x, y)}
            }
        ))
        
        return keyframes
    
    def _create_wave_pose(
        self, 
        x: float, 
        y: float, 
        hand: str, 
        amplitude: float,
        phase: str
    ) -> Dict[str, Dict[str, float]]:
        """
        创建挥手姿势
        
        Args:
            x, y: 中心坐标
            hand: 挥手的手
            amplitude: 挥手幅度
            phase: "rising" | "peak" | "falling"
        """
        base_pose = self.get_standing_pose(x, y)
        
        if phase in ["rising", "peak", "falling"]:
            # 手臂抬高
            if hand in ["right", "both"]:
                base_pose["right_hand"] = {
                    "x": x + 60,
                    "y": y - amplitude
                }
                base_pose["right_shoulder"] = {
                    "x": x + 20,
                    "y": y - 35
                }
            
            if hand in ["left", "both"]:
                base_pose["left_hand"] = {
                    "x": x - 60,
                    "y": y - amplitude
                }
                base_pose["left_shoulder"] = {
                    "x": x - 20,
                    "y": y - 35
                }
        
        return base_pose
    
    def get_duration(self, params: Dict[str, Any]) -> int:
        """获取动作时长"""
        repeat = params.get("repeat", 1)
        style = params.get("style", "normal")
        duration_per_wave = 500 if style == "enthusiastic" else 700
        return duration_per_wave * repeat
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数"""
        hand = params.get("hand", "right")
        repeat = params.get("repeat", 1)
        
        if hand not in ["left", "right", "both"]:
            return False
        if not (1 <= repeat <= 3):
            return False
        
        return True
