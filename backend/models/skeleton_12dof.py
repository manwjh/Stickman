"""
12 DOF Skeleton System (Balanced)
12自由度骨骼系统 - 平衡版

关节列表（12个）：
1. head - 头部
2. neck - 颈部
3. waist - 腰部
4. left_shoulder - 左肩
5. left_hand - 左手
6. right_shoulder - 右肩
7. right_hand - 右手
8. left_hip - 左髋
9. left_foot - 左脚
10. right_hip - 右髋
11. right_foot - 右脚
12. center - 身体中心（可选，用于位置参考）

特点：
- 省略肘部和膝盖，简化控制
- 保留关键表现力
- LLM生成准确率较高
- 适合大多数动作场景

Author: Shenzhen Wang & AI
License: MIT
"""
import math
from typing import Dict, Any, List, Tuple, Union
from dataclasses import dataclass
from backend.models.base_skeleton import BaseSkeleton, SkeletonConfig
from backend.models.skeleton_config_loader import get_skeleton_config


@dataclass
class Joint:
    """关节坐标"""
    x: float
    y: float
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {"x": self.x, "y": self.y}


class Skeleton12DOF(BaseSkeleton):
    """12自由度火柴人骨骼系统"""
    
    def __init__(self, config: SkeletonConfig = None):
        """
        初始化12DOF系统
        
        Args:
            config: 骨骼配置，如果不提供则从配置文件加载
        """
        if config is None:
            config = get_skeleton_config('12dof')
        
        super().__init__(config)
        
        # 从配置加载骨骼长度
        self.BONE_LENGTHS = config.bone_lengths
        
        # 从配置加载容差
        self.TOLERANCE = config.tolerance
        
        # 创建默认姿势
        self.default_joints = self._create_default_pose()
    
    def get_data_field_name(self) -> str:
        """获取数据字段名称"""
        return "joints"
    
    def get_default_pose(self) -> Dict[str, Any]:
        """获取默认姿态"""
        return {name: joint.to_dict() for name, joint in self.default_joints.items()}
    
    def _create_default_pose(self) -> Dict[str, Joint]:
        """创建默认站立姿势"""
        center_x, center_y = 400, 300
        
        return {
            "head": Joint(center_x, center_y - 60),
            "neck": Joint(center_x, center_y - 40),
            "waist": Joint(center_x, center_y + 20),
            "left_shoulder": Joint(center_x - 20, center_y - 35),
            "left_hand": Joint(center_x - 50, center_y + 10),
            "right_shoulder": Joint(center_x + 20, center_y - 35),
            "right_hand": Joint(center_x + 50, center_y + 10),
            "left_hip": Joint(center_x - 15, center_y + 20),
            "left_foot": Joint(center_x - 15, center_y + 70),
            "right_hip": Joint(center_x + 15, center_y + 20),
            "right_foot": Joint(center_x + 15, center_y + 70),
        }
    
    def get_system_prompt(self) -> str:
        """获取LLM系统提示词"""
        bone_lengths = self.BONE_LENGTHS
        return f"""你是一位专业动画师。你的任务是使用**12个关节**来描述火柴人动作。

🔹 12自由度系统 - 关节列表：
躯干（3个）：
  - head: 头部中心
  - neck: 颈部（头部下方）
  - waist: 腰部（身体底部）

手臂（4个，无肘部）：
  - left_shoulder: 左肩
  - left_hand: 左手
  - right_shoulder: 右肩
  - right_hand: 右手

腿部（4个，无膝盖）：
  - left_hip: 左髋
  - left_foot: 左脚
  - right_hip: 右髋
  - right_foot: 右脚

📐 标准比例（120px高）：
- 头部半径: {bone_lengths.get('head_radius', 20)}px
- 头到颈: {bone_lengths.get('neck_to_head', 20)}px
- 颈到腰: {bone_lengths.get('neck_to_waist', 60)}px
- 肩宽: {bone_lengths.get('shoulder_width', 40)}px
- 臂长: {bone_lengths.get('arm_length', 50)}px
- 髋宽: {bone_lengths.get('hip_width', 30)}px
- 腿长: {bone_lengths.get('leg_length', 50)}px

⚠️ 重要约束：
1. 骨骼长度应保持相对一致（允许±30-60%变化用于夸张动作）
2. 左右对称部位（肩宽、髋宽）应该相等
3. 身体不能断开（关节必须合理连接）
4. 画布范围：{self.config.canvas_width}x{self.config.canvas_height}px

📋 参考姿势示例：

站立姿势：
{{
  "head": {{"x": 400, "y": 240}},
  "neck": {{"x": 400, "y": 260}},
  "waist": {{"x": 400, "y": 320}},
  "left_shoulder": {{"x": 380, "y": 265}},
  "left_hand": {{"x": 350, "y": 310}},
  "right_shoulder": {{"x": 420, "y": 265}},
  "right_hand": {{"x": 450, "y": 310}},
  "left_hip": {{"x": 385, "y": 320}},
  "left_foot": {{"x": 385, "y": 370}},
  "right_hip": {{"x": 415, "y": 320}},
  "right_foot": {{"x": 415, "y": 370}}
}}

返回 JSON 格式（包含3-5个关键帧形成流畅动画）：
{{
  "characters": [{{"id": "char1", "name": "角色名", "color": "#2196F3"}}],
  "keyframes": [
    {{
      "timestamp_ms": 0,
      "description": "起始姿势",
      "characters": {{
        "char1": {{
          "dof": 12,
          "joints": {{
            "head": {{"x": 400, "y": 240}},
            "neck": {{"x": 400, "y": 260}},
            "waist": {{"x": 400, "y": 320}},
            "left_shoulder": {{"x": 380, "y": 265}},
            "left_hand": {{"x": 350, "y": 310}},
            "right_shoulder": {{"x": 420, "y": 265}},
            "right_hand": {{"x": 450, "y": 310}},
            "left_hip": {{"x": 385, "y": 320}},
            "left_foot": {{"x": 385, "y": 370}},
            "right_hip": {{"x": 415, "y": 320}},
            "right_foot": {{"x": 415, "y": 370}}
          }}
        }}
      }}
    }},
    // 更多关键帧...
  ]
}}
"""
    
    def _calculate_distance(self, j1: Dict[str, float], j2: Dict[str, float]) -> float:
        """计算两个关节之间的距离"""
        return math.sqrt((j1["x"] - j2["x"])**2 + (j1["y"] - j2["y"])**2)
    
    def validate(self, data: Union[Dict[str, Dict[str, float]], Any]) -> List[str]:
        """
        验证12DOF关节的有效性（实现抽象方法）
        
        Args:
            data: 关节字典
            
        Returns:
            错误列表，空列表表示验证通过
        """
        if not isinstance(data, dict):
            return ["数据格式错误：必须是字典类型"]
        
        return self.validate_joints(data)
    
    def validate_joints(self, joints: Dict[str, Dict[str, float]]) -> List[str]:
        """
        验证12DOF关节的有效性（保持兼容性）
        
        Args:
            joints: 关节字典
            
        Returns:
            错误列表，空列表表示验证通过
        """
        errors = []
        
        # 检查必需关节是否存在
        required = ["head", "neck", "waist",
                   "left_shoulder", "left_hand", "right_shoulder", "right_hand",
                   "left_hip", "left_foot", "right_hip", "right_foot"]
        
        for joint_name in required:
            if joint_name not in joints:
                errors.append(f"缺少关节: {joint_name}")
                return errors  # 缺少关节则无法继续验证
        
        # 检查骨骼长度
        bone_checks = [
            ("neck_to_head", "neck", "head", self.BONE_LENGTHS.get("neck_to_head", 20)),
            ("neck_to_waist", "neck", "waist", self.BONE_LENGTHS.get("neck_to_waist", 60)),
            ("left_arm", "left_shoulder", "left_hand", self.BONE_LENGTHS.get("arm_length", 50)),
            ("right_arm", "right_shoulder", "right_hand", self.BONE_LENGTHS.get("arm_length", 50)),
            ("left_leg", "left_hip", "left_foot", self.BONE_LENGTHS.get("leg_length", 50)),
            ("right_leg", "right_hip", "right_foot", self.BONE_LENGTHS.get("leg_length", 50)),
        ]
        
        for bone_name, j1_name, j2_name, expected_length in bone_checks:
            actual_length = self._calculate_distance(joints[j1_name], joints[j2_name])
            tolerance = self.TOLERANCE.get(bone_name, 0.5)
            min_allowed = expected_length * (1 - tolerance)
            max_allowed = expected_length * (1 + tolerance)
            
            if actual_length < min_allowed or actual_length > max_allowed:
                deviation = abs(actual_length - expected_length) / expected_length * 100
                errors.append(
                    f"骨骼 {bone_name} 长度异常: {actual_length:.1f}px "
                    f"(期望{expected_length}px ±{tolerance*100:.0f}%, 偏差{deviation:.1f}%)"
                )
        
        # 使用基类的画布边界验证
        for joint_name, joint in joints.items():
            errors.extend(
                self.validate_canvas_bounds(joint["x"], joint["y"], joint_name)
            )
        
        return errors
