"""
Context Memory System
上下文记忆系统 - 保障动画连续性

功能：
- 存储前N帧的关节信息
- 追踪角色状态（位置、速度、方向）
- 生成带上下文的prompt
- 检测动作异常跳变
- 支持统一的骨骼系统接口

Author: Shenzhen Wang & AI
License: MIT
"""
from typing import Dict, Any, List, Optional
from collections import deque
import math


class ContextMemory:
    """上下文记忆系统"""
    
    def __init__(self, window_size: int = 3, dof_level: str = '12dof'):
        """
        初始化上下文记忆
        
        Args:
            window_size: 滑动窗口大小，保留最近N帧
            dof_level: '6dof' 或 '12dof'
        """
        self.window_size = window_size
        self.dof_level = dof_level
        self.frame_history = deque(maxlen=window_size)
        self.character_states = {}  # {char_id: state_dict}
    
    def add_frame(self, frame_data: Dict[str, Any], char_id: str = "char1"):
        """
        添加新的帧到记忆中（统一接口）
        
        Args:
            frame_data: 帧数据（6DOF的pose或12DOF的joints）
            char_id: 角色ID
        """
        self.frame_history.append({
            "char_id": char_id,
            "data": frame_data,  # 改名为data，更通用
            "timestamp": len(self.frame_history)
        })
        
        # 更新角色状态
        self._update_character_state(char_id, frame_data)
    
    def _update_character_state(self, char_id: str, data: Dict[str, Any]):
        """
        更新角色状态（位置、速度等）- 统一接口
        
        Args:
            data: 帧数据（6DOF的pose或12DOF的joints）
        """
        if char_id not in self.character_states:
            self.character_states[char_id] = {
                "center": None,
                "velocity": {"x": 0, "y": 0},
                "facing": "right"
            }
        
        state = self.character_states[char_id]
        
        # 根据DOF类型提取中心位置
        current_center = self._extract_center_position(data)
        
        if current_center is None:
            current_center = {"x": 400, "y": 300}
        
        # 计算速度
        if state["center"] is not None:
            state["velocity"]["x"] = current_center["x"] - state["center"]["x"]
            state["velocity"]["y"] = current_center["y"] - state["center"]["y"]
        
        # 判断朝向
        if self.dof_level == '12dof':
            if "left_hand" in data and "right_hand" in data:
                if isinstance(data["right_hand"], dict) and isinstance(data["left_hand"], dict):
                    if data["right_hand"].get("x", 0) > data["left_hand"].get("x", 0):
                        state["facing"] = "right"
                    else:
                        state["facing"] = "left"
        # 6DOF暂不实现朝向判断
        
        state["center"] = current_center
    
    def _extract_center_position(self, data: Dict[str, Any]) -> Optional[Dict[str, float]]:
        """
        从数据中提取中心位置（统一接口）
        
        Args:
            data: 6DOF的pose或12DOF的joints
            
        Returns:
            中心位置 {"x": x, "y": y}，失败返回None
        """
        if self.dof_level == '12dof':
            # 12DOF：从joints中提取
            if "waist" in data and isinstance(data["waist"], dict):
                return data["waist"]
            elif "chest" in data and isinstance(data["chest"], dict):
                return data["chest"]
            else:
                # Fallback：计算平均位置
                try:
                    x_coords = [j["x"] for j in data.values() if isinstance(j, dict) and "x" in j]
                    y_coords = [j["y"] for j in data.values() if isinstance(j, dict) and "y" in j]
                    if x_coords and y_coords:
                        return {
                            "x": sum(x_coords) / len(x_coords),
                            "y": sum(y_coords) / len(y_coords)
                        }
                except:
                    pass
        
        elif self.dof_level == '6dof':
            # 6DOF：从pose中提取
            if "head_x" in data and "head_y" in data:
                return {"x": data["head_x"], "y": data["head_y"] + 40}
        
        return None
    
    def get_last_frame(self, char_id: str = "char1") -> Optional[Dict[str, Any]]:
        """获取最后一帧"""
        for frame in reversed(self.frame_history):
            if frame["char_id"] == char_id:
                return frame["data"]  # 返回data字段
        return None
    
    def get_context_prompt(self, next_action: str, char_id: str = "char1") -> str:
        """
        生成带上下文的prompt
        
        Args:
            next_action: 下一个动作描述
            char_id: 角色ID
            
        Returns:
            增强的prompt，包含上下文信息
        """
        if not self.frame_history:
            return f"请为以下姿势生成关节坐标：\n\n{next_action}"
        
        last_frame = self.get_last_frame(char_id)
        if not last_frame:
            return f"请为以下姿势生成关节坐标：\n\n{next_action}"
        
        state = self.character_states.get(char_id, {})
        
        # 构建上下文提示
        context_parts = [
            "🎯 任务：生成新的关键帧姿势",
            "",
            f"📝 新姿势描述：{next_action}",
            "",
            "⚠️ 重要：上一帧仅作为参考，你必须根据新的姿势描述生成完全不同的关节坐标！",
            "不要直接复制上一帧的坐标，必须体现出新姿势的变化！",
            ""
        ]
        
        # 添加前一帧信息（仅作参考）
        context_parts.append("📍 上一帧参考数据（不要直接复制）：")
        
        # 提取实际的数据（data字段就是joints或pose数据）
        last_data = last_frame.get("data", {})
        
        # 根据DOF类型显示数据
        if self.dof_level == '6dof':
            # 6DOF：显示角度
            context_parts.append("  6DOF姿态（角度表示）：")
            for key in ["head_x", "head_y", "body_angle", "left_arm_angle", "right_arm_angle", 
                       "left_leg_angle", "right_leg_angle"]:
                if key in last_data:
                    value = last_data[key]
                    if "angle" in key:
                        context_parts.append(f"  - {key}: {value:.1f}°")
                    else:
                        context_parts.append(f"  - {key}: {value:.1f}px")
        elif self.dof_level == '12dof':
            # 12DOF：显示关键关节坐标
            context_parts.append("  12DOF关节（坐标表示）：")
            key_joints = ["head", "neck", "waist", "left_hand", "right_hand", "left_foot", "right_foot"]
            for joint_name in key_joints:
                if joint_name in last_data and isinstance(last_data[joint_name], dict):
                    j = last_data[joint_name]
                    context_parts.append(f"  - {joint_name}: ({j.get('x', 0):.1f}, {j.get('y', 0):.1f})")
        
        # 添加状态信息
        if state.get("center"):
            center = state["center"]
            velocity = state["velocity"]
            context_parts.append("")
            context_parts.append(f"当前位置：({center['x']:.1f}, {center['y']:.1f})")
            context_parts.append(f"移动速度：({velocity['x']:.1f}, {velocity['y']:.1f}) px/frame")
            context_parts.append(f"朝向：{state.get('facing', 'unknown')}")
        
        # 添加连续性要求
        context_parts.append("")
        context_parts.append("✅ 生成新姿势时的要求：")
        context_parts.append("1. 根据新的姿势描述，生成与之匹配的关节坐标（不是复制上一帧）")
        context_parts.append("2. 确保动作流畅过渡，关节移动不要过大（避免突兀跳变）")
        context_parts.append("3. 保持骨骼长度一致性（手臂、腿部长度不变）")
        context_parts.append("4. 体现出新姿势的特征变化（如果是挥手，手臂位置必须改变）")
        
        return "\n".join(context_parts)
    
    def check_discontinuity(
        self, 
        new_joints: Dict[str, Dict[str, float]], 
        char_id: str = "char1",
        threshold: float = 100.0
    ) -> List[str]:
        """
        检查新帧是否与前一帧有异常跳变
        
        Args:
            new_joints: 新的关节数据
            char_id: 角色ID
            threshold: 跳变阈值（像素）
            
        Returns:
            警告列表
        """
        warnings = []
        
        last_frame = self.get_last_frame(char_id)
        if not last_frame:
            return warnings
        
        last_joints = last_frame["joints"]
        
        # 检查每个关节的移动距离
        for joint_name in new_joints:
            if joint_name in last_joints:
                old_j = last_joints[joint_name]
                new_j = new_joints[joint_name]
                
                distance = math.sqrt(
                    (new_j["x"] - old_j["x"])**2 + 
                    (new_j["y"] - old_j["y"])**2
                )
                
                if distance > threshold:
                    warnings.append(
                        f"关节 {joint_name} 移动距离过大: {distance:.1f}px "
                        f"(阈值: {threshold}px)"
                    )
        
        return warnings
    
    def clear(self):
        """清空记忆"""
        self.frame_history.clear()
        self.character_states.clear()
    
    def get_summary(self) -> Dict[str, Any]:
        """获取记忆摘要"""
        return {
            "frame_count": len(self.frame_history),
            "window_size": self.window_size,
            "character_states": self.character_states
        }
