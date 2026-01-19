"""
Simple 6-DOF Stick Figure Animation System

6个基本部分的简化火柴人系统：
1. head - 头部（位置）
2. body - 身体（位置 + 角度）
3. left_arm - 左臂（角度）
4. right_arm - 右臂（角度）
5. left_leg - 左腿（角度）
6. right_leg - 右腿（角度）

Author: AI Assistant
License: MIT
"""
from typing import Dict, Any, List
from dataclasses import dataclass
import math


@dataclass
class SimplePose:
    """简单的6自由度姿态"""
    head_x: float  # 头部X位置
    head_y: float  # 头部Y位置
    body_angle: float  # 身体角度（度）
    left_arm_angle: float  # 左臂角度（度）
    right_arm_angle: float  # 右臂角度（度）
    left_leg_angle: float  # 左腿角度（度）
    right_leg_angle: float  # 右腿角度（度）


class Simple6DOFSystem:
    """6自由度火柴人系统"""
    
    # 身体比例（像素）
    HEAD_RADIUS = 20
    BODY_LENGTH = 60
    ARM_LENGTH = 40
    LEG_LENGTH = 50
    
    def __init__(self):
        """初始化系统"""
        self.default_pose = SimplePose(
            head_x=400,
            head_y=300,
            body_angle=0,      # 垂直
            left_arm_angle=-45,  # 左臂
            right_arm_angle=45,  # 右臂
            left_leg_angle=-10,  # 左腿
            right_leg_angle=10   # 右腿
        )
    
    def pose_to_16joints(self, pose: SimplePose) -> Dict[str, Dict[str, float]]:
        """
        将6DOF姿态转换为关节坐标格式
        用于与渲染系统对接
        """
        # 计算身体角度的弧度
        body_rad = math.radians(pose.body_angle)
        
        # 头部
        head = {"x": pose.head_x, "y": pose.head_y}
        
        # 身体中心线
        body_base_x = pose.head_x
        body_base_y = pose.head_y + self.HEAD_RADIUS
        
        # 颈部（头部下方）
        neck = {
            "x": body_base_x,
            "y": body_base_y
        }
        
        # 胸部（身体1/3处）
        chest = {
            "x": body_base_x + math.sin(body_rad) * self.BODY_LENGTH * 0.33,
            "y": body_base_y + math.cos(body_rad) * self.BODY_LENGTH * 0.33
        }
        
        # 腰部（身体底部）
        waist = {
            "x": body_base_x + math.sin(body_rad) * self.BODY_LENGTH,
            "y": body_base_y + math.cos(body_rad) * self.BODY_LENGTH
        }
        
        # 肩膀位置（胸部两侧）
        shoulder_offset = 20
        left_shoulder = {
            "x": chest["x"] - math.cos(body_rad) * shoulder_offset,
            "y": chest["y"] + math.sin(body_rad) * shoulder_offset
        }
        right_shoulder = {
            "x": chest["x"] + math.cos(body_rad) * shoulder_offset,
            "y": chest["y"] - math.sin(body_rad) * shoulder_offset
        }
        
        # 左臂（从肩膀开始）
        left_arm_rad = math.radians(pose.left_arm_angle)
        left_elbow = {
            "x": left_shoulder["x"] + math.cos(left_arm_rad) * self.ARM_LENGTH * 0.5,
            "y": left_shoulder["y"] + math.sin(left_arm_rad) * self.ARM_LENGTH * 0.5
        }
        left_hand = {
            "x": left_shoulder["x"] + math.cos(left_arm_rad) * self.ARM_LENGTH,
            "y": left_shoulder["y"] + math.sin(left_arm_rad) * self.ARM_LENGTH
        }
        
        # 右臂（从肩膀开始）
        right_arm_rad = math.radians(pose.right_arm_angle)
        right_elbow = {
            "x": right_shoulder["x"] + math.cos(right_arm_rad) * self.ARM_LENGTH * 0.5,
            "y": right_shoulder["y"] + math.sin(right_arm_rad) * self.ARM_LENGTH * 0.5
        }
        right_hand = {
            "x": right_shoulder["x"] + math.cos(right_arm_rad) * self.ARM_LENGTH,
            "y": right_shoulder["y"] + math.sin(right_arm_rad) * self.ARM_LENGTH
        }
        
        # 髋部位置（腰部两侧）
        hip_offset = 10
        left_hip = {
            "x": waist["x"] - math.cos(body_rad) * hip_offset,
            "y": waist["y"] + math.sin(body_rad) * hip_offset
        }
        right_hip = {
            "x": waist["x"] + math.cos(body_rad) * hip_offset,
            "y": waist["y"] - math.sin(body_rad) * hip_offset
        }
        
        # 左腿（从髋部开始）
        left_leg_rad = math.radians(pose.left_leg_angle)
        left_knee = {
            "x": left_hip["x"] + math.sin(left_leg_rad) * self.LEG_LENGTH * 0.5,
            "y": left_hip["y"] + math.cos(left_leg_rad) * self.LEG_LENGTH * 0.5
        }
        left_foot = {
            "x": left_hip["x"] + math.sin(left_leg_rad) * self.LEG_LENGTH,
            "y": left_hip["y"] + math.cos(left_leg_rad) * self.LEG_LENGTH
        }
        
        # 右腿（从髋部开始）
        right_leg_rad = math.radians(pose.right_leg_angle)
        right_knee = {
            "x": right_hip["x"] + math.sin(right_leg_rad) * self.LEG_LENGTH * 0.5,
            "y": right_hip["y"] + math.cos(right_leg_rad) * self.LEG_LENGTH * 0.5
        }
        right_foot = {
            "x": right_hip["x"] + math.sin(right_leg_rad) * self.LEG_LENGTH,
            "y": right_hip["y"] + math.cos(right_leg_rad) * self.LEG_LENGTH
        }
        
        # 返回关节坐标格式
        return {
            "head": head,
            "neck": neck,
            "chest": chest,
            "waist": waist,
            "left_shoulder": left_shoulder,
            "left_elbow": left_elbow,
            "left_hand": left_hand,
            "right_shoulder": right_shoulder,
            "right_elbow": right_elbow,
            "right_hand": right_hand,
            "left_hip": left_hip,
            "left_knee": left_knee,
            "left_foot": left_foot,
            "right_hip": right_hip,
            "right_knee": right_knee,
            "right_foot": right_foot
        }
    
    def simple_to_animation(self, keyframes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        将简单格式的关键帧转换为完整动画数据
        
        输入格式：
        {
            "keyframes": [
                {
                    "timestamp_ms": 0,
                    "description": "站立",
                    "pose": {
                        "head_x": 400,
                        "head_y": 300,
                        "body_angle": 0,
                        "left_arm_angle": -45,
                        "right_arm_angle": 45,
                        "left_leg_angle": -10,
                        "right_leg_angle": 10
                    }
                }
            ]
        }
        
        输出格式：关节坐标字典
        """
        converted_keyframes = []
        
        for kf in keyframes:
            pose_data = kf.get("pose", {})
            pose = SimplePose(
                head_x=pose_data.get("head_x", 400),
                head_y=pose_data.get("head_y", 300),
                body_angle=pose_data.get("body_angle", 0),
                left_arm_angle=pose_data.get("left_arm_angle", -45),
                right_arm_angle=pose_data.get("right_arm_angle", 45),
                left_leg_angle=pose_data.get("left_leg_angle", -10),
                right_leg_angle=pose_data.get("right_leg_angle", 10)
            )
            
            # 转换为关节坐标
            joints_16 = self.pose_to_16joints(pose)
            
            converted_keyframes.append({
                "timestamp_ms": kf.get("timestamp_ms", 0),
                "description": kf.get("description", ""),
                "characters": {
                    "char1": joints_16
                }
            })
        
        return {
            "characters": [
                {"id": "char1", "name": "Character", "color": "#2196F3"}
            ],
            "keyframes": converted_keyframes
        }


# 测试函数
def test_simple_system():
    """测试6自由度系统"""
    system = Simple6DOFSystem()
    
    # 测试姿态
    test_poses = [
        # 站立
        SimplePose(400, 300, 0, -45, 45, -10, 10),
        # 举手欢呼
        SimplePose(400, 280, 0, -160, -160, -15, 15),
        # 弯腰
        SimplePose(400, 320, 30, -20, 20, -5, 5),
    ]
    
    print("6自由度系统测试\n" + "="*50)
    
    for i, pose in enumerate(test_poses):
        print(f"\n姿态 {i+1}:")
        joints = system.pose_to_16joints(pose)
        print(f"  头部: ({joints['head']['x']:.1f}, {joints['head']['y']:.1f})")
        print(f"  腰部: ({joints['waist']['x']:.1f}, {joints['waist']['y']:.1f})")
        print(f"  左手: ({joints['left_hand']['x']:.1f}, {joints['left_hand']['y']:.1f})")
        print(f"  右脚: ({joints['right_foot']['x']:.1f}, {joints['right_foot']['y']:.1f})")
    
    print("\n✅ 6自由度系统测试完成")


if __name__ == "__main__":
    test_simple_system()
