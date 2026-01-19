"""
Animation Optimizer - Level 3 (V2)
动画优化器 - 验证、修正、优化

功能:
1. 约束验证
2. 自动修正简单错误 (算法)
3. 高级插值和平滑
4. 无法修正时整体重新生成

Author: Shenzhen Wang & AI
License: MIT
"""
import logging
import math
from typing import Dict, Any, List, Tuple, Optional
from backend.models.base_skeleton import BaseSkeleton
from backend.models.skeleton_factory import create_skeleton

logger = logging.getLogger(__name__)


class AnimationOptimizer:
    """动画优化器 - 验证、修正、优化"""
    
    def __init__(self, dof_level: str = "12dof"):
        """
        初始化优化器
        
        Args:
            dof_level: 骨骼自由度
        """
        self.dof_level = dof_level
        self.skeleton = create_skeleton(dof_level)
        logger.info(f"Animation Optimizer V2 initialized (dof={dof_level})")
    
    def optimize(
        self, 
        animation_data: Dict[str, Any],
        auto_fix: bool = True,
        interpolate: bool = True,
        target_fps: int = 30
    ) -> Dict[str, Any]:
        """
        优化动画数据
        
        Args:
            animation_data: 动画数据
            auto_fix: 是否自动修正错误
            interpolate: 是否进行插值
            target_fps: 目标帧率（插值时使用）
            
        Returns:
            优化后的动画数据
        """
        keyframes = animation_data.get("keyframes", [])
        
        if not keyframes:
            raise ValueError("No keyframes to optimize")
        
        logger.info(f"Optimizing {len(keyframes)} keyframes...")
        
        # Step 1: 验证
        is_valid, errors = self._validate_all_keyframes(keyframes)
        
        if not is_valid:
            logger.warning(f"Found {len(errors)} validation errors")
            
            if auto_fix:
                # Step 2: 自动修正
                keyframes = self._auto_fix_errors(keyframes, errors)
                
                # 重新验证
                is_valid_after_fix, errors_after_fix = self._validate_all_keyframes(keyframes)
                
                if is_valid_after_fix:
                    logger.info("自动修正成功，所有错误已修复")
                else:
                    logger.warning(f"自动修正后仍有 {len(errors_after_fix)} 个错误")
        
        # Step 3: 插值（可选，生成所有帧）
        if interpolate:
            keyframes = self._interpolate_keyframes(keyframes, target_fps)
            logger.info(f"插值后共 {len(keyframes)} 帧 ({target_fps}fps)")
        
        # 更新动画数据
        animation_data["keyframes"] = keyframes
        animation_data["optimized"] = True
        animation_data["target_fps"] = target_fps if interpolate else None
        
        return animation_data
    
    def _validate_all_keyframes(
        self, 
        keyframes: List[Dict[str, Any]]
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        验证所有关键帧
        
        Returns:
            (是否有效, 错误列表)
        """
        all_errors = []
        
        for i, kf in enumerate(keyframes):
            errors = self._validate_keyframe(kf, i)
            if errors:
                all_errors.extend(errors)
        
        is_valid = len(all_errors) == 0
        return is_valid, all_errors
    
    def _validate_keyframe(
        self, 
        keyframe: Dict[str, Any],
        index: int
    ) -> List[Dict[str, Any]]:
        """
        验证单个关键帧
        
        Returns:
            错误列表
        """
        errors = []
        
        if "characters" not in keyframe:
            errors.append({
                "keyframe_index": index,
                "type": "missing_field",
                "message": "缺少characters字段"
            })
            return errors
        
        characters = keyframe["characters"]
        
        for char_id, char_data in characters.items():
            data_field = self.skeleton.get_data_field_name()
            
            if data_field not in char_data:
                errors.append({
                    "keyframe_index": index,
                    "character_id": char_id,
                    "type": "missing_field",
                    "message": f"缺少{data_field}字段"
                })
                continue
            
            # 使用骨骼系统验证
            validation_errors = self.skeleton.validate(char_data[data_field])
            
            for err in validation_errors:
                errors.append({
                    "keyframe_index": index,
                    "character_id": char_id,
                    "type": "constraint_violation",
                    "message": err
                })
        
        return errors
    
    def _auto_fix_errors(
        self,
        keyframes: List[Dict[str, Any]],
        errors: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        自动修正错误
        
        Args:
            keyframes: 关键帧列表
            errors: 错误列表
            
        Returns:
            修正后的关键帧列表
        """
        # 按关键帧索引分组错误
        errors_by_keyframe = {}
        for error in errors:
            kf_idx = error.get("keyframe_index", -1)
            if kf_idx not in errors_by_keyframe:
                errors_by_keyframe[kf_idx] = []
            errors_by_keyframe[kf_idx].append(error)
        
        # 修正每个关键帧
        for kf_idx, kf_errors in errors_by_keyframe.items():
            if 0 <= kf_idx < len(keyframes):
                keyframes[kf_idx] = self._fix_keyframe(
                    keyframes[kf_idx], 
                    kf_errors
                )
        
        return keyframes
    
    def _fix_keyframe(
        self,
        keyframe: Dict[str, Any],
        errors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        修正单个关键帧
        
        Args:
            keyframe: 关键帧
            errors: 该关键帧的错误列表
            
        Returns:
            修正后的关键帧
        """
        for error in errors:
            error_type = error.get("type")
            message = error.get("message", "")
            
            if error_type == "constraint_violation":
                # 尝试修正约束违规
                if "骨骼" in message and "长度异常" in message:
                    keyframe = self._fix_bone_length(keyframe, error)
                elif "坐标超出" in message:
                    keyframe = self._fix_canvas_bounds(keyframe, error)
        
        return keyframe
    
    def _fix_bone_length(
        self,
        keyframe: Dict[str, Any],
        error: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        修正骨骼长度错误
        
        策略: 保持方向，调整长度
        """
        # TODO: 实现骨骼长度自动修正
        # 这需要解析错误消息，提取骨骼名称和期望长度
        logger.debug(f"尝试修正骨骼长度: {error.get('message')}")
        return keyframe
    
    def _fix_canvas_bounds(
        self,
        keyframe: Dict[str, Any],
        error: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        修正画布边界错误
        
        策略: 将超出部分约束到边界内
        """
        char_id = error.get("character_id")
        if not char_id:
            return keyframe
        
        characters = keyframe.get("characters", {})
        if char_id not in characters:
            return keyframe
        
        char_data = characters[char_id]
        data_field = self.skeleton.get_data_field_name()
        
        if data_field not in char_data:
            return keyframe
        
        joints = char_data[data_field]
        
        # 约束所有关节到画布内
        for joint_name, joint in joints.items():
            if isinstance(joint, dict) and "x" in joint and "y" in joint:
                joint["x"] = max(0, min(800, joint["x"]))
                joint["y"] = max(0, min(600, joint["y"]))
        
        return keyframe
    
    def _interpolate_keyframes(
        self,
        keyframes: List[Dict[str, Any]],
        target_fps: int = 30
    ) -> List[Dict[str, Any]]:
        """
        在关键帧之间插值，生成所有帧
        
        Args:
            keyframes: 关键帧列表
            target_fps: 目标帧率
            
        Returns:
            插值后的帧列表（包含所有中间帧）
        """
        if len(keyframes) < 2:
            return keyframes
        
        interpolated = []
        
        for i in range(len(keyframes) - 1):
            kf1 = keyframes[i]
            kf2 = keyframes[i + 1]
            
            interpolated.append(kf1)
            
            # 计算需要插入多少帧
            time_diff = kf2["timestamp_ms"] - kf1["timestamp_ms"]
            if time_diff <= 0:
                continue
            
            frame_interval = 1000 / target_fps  # 每帧时长(ms)
            num_frames = int(time_diff / frame_interval) - 1
            
            if num_frames > 0:
                # 线性插值
                for j in range(1, num_frames + 1):
                    t = j / (num_frames + 1)
                    interp_frame = self._lerp_keyframes(kf1, kf2, t)
                    interpolated.append(interp_frame)
        
        # 添加最后一帧
        interpolated.append(keyframes[-1])
        
        return interpolated
    
    def _lerp_keyframes(
        self,
        kf1: Dict[str, Any],
        kf2: Dict[str, Any],
        t: float
    ) -> Dict[str, Any]:
        """
        在两个关键帧之间线性插值
        
        Args:
            kf1: 第一个关键帧
            kf2: 第二个关键帧
            t: 插值参数 (0-1)
            
        Returns:
            插值后的帧
        """
        timestamp = int(kf1["timestamp_ms"] + (kf2["timestamp_ms"] - kf1["timestamp_ms"]) * t)
        
        interpolated = {
            "timestamp_ms": timestamp,
            "description": f"插值帧 (t={t:.2f})",
            "characters": {}
        }
        
        # 为每个角色插值
        for char_id in kf1.get("characters", {}).keys():
            if char_id not in kf2.get("characters", {}):
                continue
            
            char1 = kf1["characters"][char_id]
            char2 = kf2["characters"][char_id]
            
            data_field = self.skeleton.get_data_field_name()
            
            if data_field not in char1 or data_field not in char2:
                continue
            
            joints1 = char1[data_field]
            joints2 = char2[data_field]
            
            # 插值关节
            interpolated_joints = {}
            for joint_name in joints1.keys():
                if joint_name not in joints2:
                    continue
                
                j1 = joints1[joint_name]
                j2 = joints2[joint_name]
                
                if isinstance(j1, dict) and isinstance(j2, dict):
                    interpolated_joints[joint_name] = {
                        "x": j1["x"] + (j2["x"] - j1["x"]) * t,
                        "y": j1["y"] + (j2["y"] - j1["y"]) * t
                    }
            
            interpolated["characters"][char_id] = {
                data_field: interpolated_joints
            }
        
        return interpolated