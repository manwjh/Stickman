"""
6 DOF Skeleton System (Classic)
6自由度骨骼系统 - 经典简化版

自由度：
1. head_x, head_y - 头部位置
2. body_angle - 身体角度
3. left_arm_angle - 左臂角度
4. right_arm_angle - 右臂角度
5. left_leg_angle - 左腿角度
6. right_leg_angle - 右腿角度

特点：
- 简单易控，LLM生成准确率高
- 适合简单动作和快速原型
- 计算开销小

Author: Shenzhen Wang & AI
License: MIT
"""
import math
from typing import Dict, Any, List, Union
from dataclasses import dataclass, asdict
from backend.models.base_skeleton import BaseSkeleton, SkeletonConfig
from backend.models.skeleton_config_loader import get_skeleton_config


@dataclass
class Pose6DOF:
    """6自由度姿态"""
    head_x: float
    head_y: float
    body_angle: float  # 度数
    left_arm_angle: float
    right_arm_angle: float
    left_leg_angle: float
    right_leg_angle: float
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return asdict(self)


class Skeleton6DOF(BaseSkeleton):
    """6自由度火柴人骨骼系统"""
    
    def __init__(self, config: SkeletonConfig = None):
        """
        初始化6DOF系统
        
        Args:
            config: 骨骼配置，如果不提供则从配置文件加载
        """
        if config is None:
            config = get_skeleton_config('6dof')
        
        super().__init__(config)
        
        # 从配置加载参数
        self.HEAD_RADIUS = config.bone_lengths.get('head_radius', 20)
        self.BODY_LENGTH = config.bone_lengths.get('body_length', 60)
        self.ARM_LENGTH = config.bone_lengths.get('arm_length', 40)
        self.LEG_LENGTH = config.bone_lengths.get('leg_length', 50)
        
        # 角度限制
        self.BODY_ANGLE_RANGE = config.angle_limits.get('body_angle', (-45, 45))
        self.ARM_ANGLE_RANGE = config.angle_limits.get('arm_angle', (-180, 180))
        self.LEG_ANGLE_RANGE = config.angle_limits.get('leg_angle', (-45, 45))
        
        # 默认姿态
        self.default_pose = Pose6DOF(
            head_x=400,
            head_y=200,
            body_angle=0,
            left_arm_angle=-45,
            right_arm_angle=45,
            left_leg_angle=-10,
            right_leg_angle=10
        )
    
    def get_data_field_name(self) -> str:
        """获取数据字段名称"""
        return "pose"
    
    def get_default_pose(self) -> Dict[str, Any]:
        """获取默认姿态"""
        return self.default_pose.to_dict()
    
    def get_system_prompt(self) -> str:
        """获取LLM系统提示词"""
        return f"""你是一位动画师。你的任务是用**6个参数**来描述火柴人动作。

🔹 6自由度系统 - 参数说明：
1. head_x, head_y - 头部位置 (x: 100-700, y: 100-400)
2. body_angle - 身体倾斜角度 (度，0=垂直，正数=向右倾，范围: {self.BODY_ANGLE_RANGE[0]}到{self.BODY_ANGLE_RANGE[1]})
3. left_arm_angle - 左臂角度 (度，0=水平向左，正数=逆时针，范围: {self.ARM_ANGLE_RANGE[0]}到{self.ARM_ANGLE_RANGE[1]})
4. right_arm_angle - 右臂角度 (度，0=水平向右，正数=顺时针，范围: {self.ARM_ANGLE_RANGE[0]}到{self.ARM_ANGLE_RANGE[1]})
5. left_leg_angle - 左腿角度 (度，0=垂直，正数=向右，范围: {self.LEG_ANGLE_RANGE[0]}到{self.LEG_ANGLE_RANGE[1]})
6. right_leg_angle - 右腿角度 (度，0=垂直，正数=向左，范围: {self.LEG_ANGLE_RANGE[0]}到{self.LEG_ANGLE_RANGE[1]})

📐 标准比例：
- 头部半径: {self.HEAD_RADIUS}px
- 身体长度: {self.BODY_LENGTH}px
- 手臂长度: {self.ARM_LENGTH}px
- 腿部长度: {self.LEG_LENGTH}px

📋 参考姿势：
- 站立：body_angle=0, left_arm=-45, right_arm=45, left_leg=-10, right_leg=10
- 举手欢呼：body_angle=0, left_arm=-160, right_arm=-160, left_leg=-15, right_leg=15
- 奔跑：body_angle=15, left_arm=-120, right_arm=30, left_leg=-30, right_leg=30
- 弯腰：body_angle=30, left_arm=-20, right_arm=20, left_leg=-5, right_leg=5

⚠️ 画布约束：{self.config.canvas_width}x{self.config.canvas_height}px

返回 JSON 格式（多个关键帧形成动画）：
{{
  "characters": [{{"id": "char1", "name": "角色名", "color": "#2196F3"}}],
  "keyframes": [
    {{
      "timestamp_ms": 0,
      "description": "开始姿势",
      "characters": {{
        "char1": {{
          "dof": 6,
          "pose": {{
            "head_x": 400,
            "head_y": 200,
            "body_angle": 0,
            "left_arm_angle": -45,
            "right_arm_angle": 45,
            "left_leg_angle": -10,
            "right_leg_angle": 10
          }}
        }}
      }}
    }},
    // 更多关键帧...
  ]
}}
"""
    
    def validate(self, data: Union[Dict[str, Any], Pose6DOF]) -> List[str]:
        """
        验证6DOF姿态的有效性（实现抽象方法）
        
        Args:
            data: Pose6DOF对象或字典
            
        Returns:
            错误列表，空列表表示验证通过
        """
        # 转换为Pose6DOF对象
        if isinstance(data, dict):
            try:
                pose = Pose6DOF(
                    head_x=data.get("head_x", 400),
                    head_y=data.get("head_y", 200),
                    body_angle=data.get("body_angle", 0),
                    left_arm_angle=data.get("left_arm_angle", -45),
                    right_arm_angle=data.get("right_arm_angle", 45),
                    left_leg_angle=data.get("left_leg_angle", -10),
                    right_leg_angle=data.get("right_leg_angle", 10)
                )
            except Exception as e:
                return [f"数据格式错误: {str(e)}"]
        else:
            pose = data
        
        return self.validate_pose(pose)
    
    def validate_pose(self, pose: Pose6DOF) -> List[str]:
        """
        验证6DOF姿态的有效性（保持兼容性）
        
        Args:
            pose: Pose6DOF对象
            
        Returns:
            错误列表，空列表表示验证通过
        """
        errors = []
        
        # 检查头部位置
        if not (100 <= pose.head_x <= 700):
            errors.append(f"head_x 超出范围: {pose.head_x} (应在100-700)")
        if not (100 <= pose.head_y <= 400):
            errors.append(f"head_y 超出范围: {pose.head_y} (应在100-400)")
        
        # 使用基类的画布边界验证
        errors.extend(self.validate_canvas_bounds(pose.head_x, pose.head_y, "head"))
        
        # 检查身体角度
        if not (self.BODY_ANGLE_RANGE[0] <= pose.body_angle <= self.BODY_ANGLE_RANGE[1]):
            errors.append(
                f"body_angle 超出范围: {pose.body_angle} "
                f"(应在{self.BODY_ANGLE_RANGE})"
            )
        
        # 检查手臂角度
        if not (self.ARM_ANGLE_RANGE[0] <= pose.left_arm_angle <= self.ARM_ANGLE_RANGE[1]):
            errors.append(f"left_arm_angle 超出范围: {pose.left_arm_angle}")
        if not (self.ARM_ANGLE_RANGE[0] <= pose.right_arm_angle <= self.ARM_ANGLE_RANGE[1]):
            errors.append(f"right_arm_angle 超出范围: {pose.right_arm_angle}")
        
        # 检查腿部角度
        if not (self.LEG_ANGLE_RANGE[0] <= pose.left_leg_angle <= self.LEG_ANGLE_RANGE[1]):
            errors.append(f"left_leg_angle 超出范围: {pose.left_leg_angle}")
        if not (self.LEG_ANGLE_RANGE[0] <= pose.right_leg_angle <= self.LEG_ANGLE_RANGE[1]):
            errors.append(f"right_leg_angle 超出范围: {pose.right_leg_angle}")
        
        return errors
