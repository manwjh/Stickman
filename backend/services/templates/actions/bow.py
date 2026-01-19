"""
Bow Template - 鞠躬动作模板
生成礼貌的鞠躬动画

Author: Shenzhen Wang & AI
License: MIT
"""
import math
from typing import Dict, Any, List
from ..template_engine import ActionTemplate, Keyframe


class BowTemplate(ActionTemplate):
    """鞠躬动作模板"""
    
    def generate(
        self, 
        character: Dict[str, Any], 
        params: Dict[str, Any]
    ) -> List[Keyframe]:
        """
        生成鞠躬动画
        
        参数:
            depth: "shallow" | "normal" | "deep" - 鞠躬深度
            hold_duration: 保持鞠躬的时长 (ms)
        """
        depth = params.get("depth", "normal")
        hold_duration = params.get("hold_duration", 500)
        
        char_id = character["id"]
        x, y = 400, 300
        
        # 根据深度确定鞠躬角度
        angles = {"shallow": 15, "normal": 30, "deep": 45}
        bow_angle = angles.get(depth, 30)
        
        # 动作时长
        bow_down_duration = 800
        hold_time = hold_duration
        bow_up_duration = 600
        total_duration = bow_down_duration + hold_time + bow_up_duration
        
        keyframes = []
        
        # 1. 站立姿势
        keyframes.append(Keyframe(
            timestamp_ms=0,
            description="准备鞠躬",
            characters={
                char_id: {"joints": self.get_standing_pose(x, y)}
            }
        ))
        
        # 2. 开始鞠躬 (中间过渡帧)
        joints_bow_mid = self._create_bow_pose(x, y, bow_angle * 0.5)
        keyframes.append(Keyframe(
            timestamp_ms=bow_down_duration // 2,
            description=f"开始鞠躬",
            characters={
                char_id: {"joints": joints_bow_mid}
            }
        ))
        
        # 3. 鞠躬到底 (身体前倾)
        joints_bow = self._create_bow_pose(x, y, bow_angle)
        keyframes.append(Keyframe(
            timestamp_ms=bow_down_duration,
            description=f"鞠躬 ({depth})",
            characters={
                char_id: {"joints": joints_bow}
            }
        ))
        
        # 4. 保持鞠躬 (可选)
        if hold_duration > 0:
            keyframes.append(Keyframe(
                timestamp_ms=bow_down_duration + hold_time,
                description="保持鞠躬姿势",
                characters={
                    char_id: {"joints": joints_bow}
                }
            ))
        
        # 5. 开始起身 (中间过渡帧)
        keyframes.append(Keyframe(
            timestamp_ms=bow_down_duration + hold_time + bow_up_duration // 2,
            description="开始起身",
            characters={
                char_id: {"joints": joints_bow_mid}
            }
        ))
        
        # 6. 完全起身
        keyframes.append(Keyframe(
            timestamp_ms=total_duration,
            description="起身恢复",
            characters={
                char_id: {"joints": self.get_standing_pose(x, y)}
            }
        ))
        
        return keyframes
    
    def _create_bow_pose(
        self, 
        x: float, 
        y: float, 
        angle: float
    ) -> Dict[str, Dict[str, float]]:
        """
        创建鞠躬姿势
        
        Args:
            x, y: 中心坐标
            angle: 鞠躬角度 (度)
        """
        # 将角度转换为弧度
        angle_rad = math.radians(angle)
        
        # 计算身体前倾
        forward_offset = math.sin(angle_rad) * 30
        down_offset = (1 - math.cos(angle_rad)) * 20
        
        return {
            "head": {
                "x": x + forward_offset,
                "y": y - 60 + down_offset
            },
            "neck": {
                "x": x + forward_offset * 0.8,
                "y": y - 40 + down_offset * 0.8
            },
            "waist": {"x": x, "y": y + 20},
            "left_shoulder": {
                "x": x - 20 + forward_offset * 0.6,
                "y": y - 35 + down_offset * 0.6
            },
            "left_hand": {
                "x": x - 30 + forward_offset * 0.4,
                "y": y + 20
            },
            "right_shoulder": {
                "x": x + 20 + forward_offset * 0.6,
                "y": y - 35 + down_offset * 0.6
            },
            "right_hand": {
                "x": x + 30 + forward_offset * 0.4,
                "y": y + 20
            },
            "left_hip": {"x": x - 15, "y": y + 20},
            "left_foot": {"x": x - 15, "y": y + 70},
            "right_hip": {"x": x + 15, "y": y + 20},
            "right_foot": {"x": x + 15, "y": y + 70}
        }
    
    def get_duration(self, params: Dict[str, Any]) -> int:
        """获取动作时长"""
        hold_duration = params.get("hold_duration", 500)
        return 800 + hold_duration + 600
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数"""
        depth = params.get("depth", "normal")
        if depth not in ["shallow", "normal", "deep"]:
            return False
        return True
