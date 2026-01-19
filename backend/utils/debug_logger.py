"""
调试数据记录器 - Debug Data Logger
保存Pipeline各个阶段的中间数据，方便问题排查

Author: Shenzhen Wang & AI
License: MIT
"""
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class DebugLogger:
    """调试数据记录器 - 保存Pipeline中间过程数据"""
    
    def __init__(self, enabled: bool = True, output_dir: str = "debug_logs"):
        """
        初始化调试记录器
        
        Args:
            enabled: 是否启用调试日志
            output_dir: 输出目录路径
        """
        self.enabled = enabled
        self.output_dir = output_dir
        self.current_session_id = None
        self.session_dir = None
        
        if self.enabled:
            self._ensure_output_dir()
            logger.info(f"Debug Logger initialized: output_dir={output_dir}")
    
    def _ensure_output_dir(self):
        """确保输出目录存在"""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def start_session(self, story: str, dof_level: str) -> str:
        """
        开始新的调试会话
        
        Args:
            story: 用户输入的故事
            dof_level: DOF级别
            
        Returns:
            session_id: 会话ID
        """
        if not self.enabled:
            return None
        
        # 生成会话ID（时间戳）
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        
        # 创建会话目录
        self.session_dir = os.path.join(self.output_dir, self.current_session_id)
        Path(self.session_dir).mkdir(parents=True, exist_ok=True)
        
        # 保存会话元数据
        metadata = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "story": story,
            "dof_level": dof_level
        }
        
        self._save_json("00_session_metadata.json", metadata)
        logger.info(f"Debug session started: {self.current_session_id}")
        
        return self.current_session_id
    
    def log_final_output(self, final_animation: Dict[str, Any], metadata: Dict[str, Any]):
        """
        记录最终输出
        
        Args:
            final_animation: 最终动画数据
            metadata: 元数据
        """
        if not self.enabled or not self.session_dir:
            return
        
        data = {
            "stage": "Final Output",
            "timestamp": datetime.now().isoformat(),
            "final_animation": final_animation,
            "metadata": metadata
        }
        
        self._save_json("06_final_output.json", data)
        logger.debug("Logged Final Output")
    
    def log_custom(self, filename: str, data: Any):
        """
        记录自定义数据
        
        Args:
            filename: 文件名
            data: 要保存的数据
        """
        if not self.enabled or not self.session_dir:
            return
        
        self._save_json(filename, {
            "timestamp": datetime.now().isoformat(),
            **data
        } if isinstance(data, dict) else {
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
        logger.debug(f"Logged custom data: {filename}")
    
    def log_error(self, error: Exception, stage: str):
        """
        记录错误信息
        
        Args:
            error: 异常对象
            stage: 出错的阶段
        """
        if not self.enabled or not self.session_dir:
            return
        
        data = {
            "stage": stage,
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "error_details": repr(error)
        }
        
        self._save_json("99_error.json", data)
        logger.debug(f"Logged Error at {stage}")
    
    def _save_json(self, filename: str, data: Any):
        """
        保存JSON数据到文件
        
        Args:
            filename: 文件名
            data: 要保存的数据
        """
        if not self.session_dir:
            return
        
        filepath = os.path.join(self.session_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save debug file {filename}: {e}")
    
    def _generate_keyframe_svgs(self, animation_data: Dict[str, Any]):
        """
        为每个关键帧生成SVG文件
        
        Args:
            animation_data: 动画数据
        """
        if not self.session_dir:
            return
        
        # 创建SVG输出目录
        svg_dir = os.path.join(self.session_dir, "keyframe_svgs")
        Path(svg_dir).mkdir(exist_ok=True)
        
        keyframes = animation_data.get("keyframes", [])
        canvas = animation_data.get("canvas", {"width": 800, "height": 600})
        characters = animation_data.get("characters", [])
        
        for idx, keyframe in enumerate(keyframes):
            try:
                svg_content = self._create_svg_for_keyframe(
                    keyframe, canvas, characters, idx
                )
                
                filename = f"keyframe_{idx:03d}.svg"
                filepath = os.path.join(svg_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                    
            except Exception as e:
                logger.error(f"Failed to generate SVG for keyframe {idx}: {e}")
        
        logger.info(f"Generated {len(keyframes)} keyframe SVG files in {svg_dir}")
    
    def _create_svg_for_keyframe(
        self, 
        keyframe: Dict[str, Any], 
        canvas: Dict[str, Any],
        characters: List[Dict[str, Any]],
        frame_index: int
    ) -> str:
        """
        为单个关键帧创建SVG内容
        
        Args:
            keyframe: 关键帧数据
            canvas: 画布配置
            characters: 角色列表
            frame_index: 帧索引
            
        Returns:
            SVG内容字符串
        """
        width = canvas.get("width", 800)
        height = canvas.get("height", 600)
        ground_y = canvas.get("ground_y", height - 50)
        
        # SVG头部
        svg_lines = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'  <rect width="{width}" height="{height}" fill="white"/>',
            f'  ',
            f'  <!-- Ground line -->',
            f'  <line x1="0" y1="{ground_y}" x2="{width}" y2="{ground_y}" stroke="#ddd" stroke-width="2"/>',
            f'  ',
            f'  <!-- Frame {frame_index} -->',
        ]
        
        # 添加旁白文字（如果有）
        narration = keyframe.get("narration", "")
        if narration:
            svg_lines.extend([
                f'  <text x="{width/2}" y="30" text-anchor="middle" font-size="16" fill="#333">',
                f'    {self._escape_xml(narration)}',
                f'  </text>',
                f'  '
            ])
        
        # 渲染每个角色
        char_poses = keyframe.get("characters", {})
        for char in characters:
            char_id = char.get("id")
            pose = char_poses.get(char_id)
            
            if not pose:
                continue
                
            color = char.get("color", "#2196F3")
            svg_lines.append(f'  <!-- Character: {char_id} -->')
            svg_lines.append(f'  <g id="char_{char_id}" class="stick-figure">')
            
            # 渲染骨骼
            svg_lines.extend(self._render_skeleton(pose, color))
            
            svg_lines.append(f'  </g>')
            svg_lines.append(f'  ')
        
        # SVG结束标签
        svg_lines.append('</svg>')
        
        return '\n'.join(svg_lines)
    
    def _render_skeleton(self, pose: Dict[str, Any], color: str) -> List[str]:
        """
        渲染骨骼结构
        
        Args:
            pose: 姿势数据（可能包含joints或已转换的线段数据）
            color: 颜色
            
        Returns:
            SVG行列表
        """
        lines = []
        
        # 检测数据格式：是关节坐标还是线段数据
        if "joints" in pose:
            # 新格式：关节坐标数据，需要转换
            joints = pose["joints"]
            dof = pose.get("dof", 12)
            
            if dof == 6:
                # 6DOF：暂不支持关节格式（需要单独实现）
                logger.warning("6DOF joints format not yet supported in SVG renderer")
                return lines
            else:
                # 12DOF：转换关节为线段
                converted_pose = self._convert_joints_to_lines(joints, dof)
                return self._render_converted_skeleton(converted_pose, color)
        else:
            # 旧格式：已经是线段数据
            # 头部
            if "head" in pose:
                head = pose["head"]
                cx, cy, r = head.get("cx", 0), head.get("cy", 0), head.get("r", 20)
                lines.append(
                    f'    <circle cx="{cx}" cy="{cy}" r="{r}" '
                    f'stroke="{color}" fill="none" stroke-width="3"/>'
                )
            
            # 检测骨骼类型
            if "left_hip_connector" in pose:
                # 12DOF
                lines.extend(self._render_12dof_skeleton(pose, color))
            else:
                # 6DOF
                lines.extend(self._render_6dof_skeleton(pose, color))
        
        return lines
    
    def _convert_joints_to_lines(self, joints: Dict[str, Dict[str, float]], dof: int) -> Dict[str, Any]:
        """
        将关节坐标转换为线段数据
        
        Args:
            joints: 关节坐标字典 {"head": {"x": 400, "y": 240}, ...}
            dof: 自由度（12 或 16）
            
        Returns:
            线段数据字典
        """
        lines = {}
        
        if dof == 12:
            # 12DOF: head, neck, waist, left_shoulder, left_hand, right_shoulder, right_hand, 
            #        left_hip, left_foot, right_hip, right_foot
            
            # 头部（圆圈）
            if "head" in joints:
                lines["head"] = {
                    "cx": joints["head"]["x"],
                    "cy": joints["head"]["y"],
                    "r": 20
                }
            
            # 颈部: head -> neck
            if "head" in joints and "neck" in joints:
                lines["neck"] = {
                    "x1": joints["head"]["x"],
                    "y1": joints["head"]["y"],
                    "x2": joints["neck"]["x"],
                    "y2": joints["neck"]["y"],
                    "stroke-width": 3
                }
            
            # 上躯干: neck -> shoulders中点
            if "neck" in joints and "left_shoulder" in joints and "right_shoulder" in joints:
                shoulder_center_x = (joints["left_shoulder"]["x"] + joints["right_shoulder"]["x"]) / 2
                shoulder_center_y = (joints["left_shoulder"]["y"] + joints["right_shoulder"]["y"]) / 2
                
                lines["upper_torso"] = {
                    "x1": joints["neck"]["x"],
                    "y1": joints["neck"]["y"],
                    "x2": shoulder_center_x,
                    "y2": shoulder_center_y,
                    "stroke-width": 4
                }
            
            # 下躯干: shoulders中点 -> waist
            if "waist" in joints and "left_shoulder" in joints and "right_shoulder" in joints:
                shoulder_center_x = (joints["left_shoulder"]["x"] + joints["right_shoulder"]["x"]) / 2
                shoulder_center_y = (joints["left_shoulder"]["y"] + joints["right_shoulder"]["y"]) / 2
                
                lines["lower_torso"] = {
                    "x1": shoulder_center_x,
                    "y1": shoulder_center_y,
                    "x2": joints["waist"]["x"],
                    "y2": joints["waist"]["y"],
                    "stroke-width": 4
                }
            
            # 肩部连接器（左右）
            if "left_shoulder" in joints and "right_shoulder" in joints:
                shoulder_center_x = (joints["left_shoulder"]["x"] + joints["right_shoulder"]["x"]) / 2
                shoulder_center_y = (joints["left_shoulder"]["y"] + joints["right_shoulder"]["y"]) / 2
                
                lines["left_shoulder_connector"] = {
                    "x1": shoulder_center_x,
                    "y1": shoulder_center_y,
                    "x2": joints["left_shoulder"]["x"],
                    "y2": joints["left_shoulder"]["y"],
                    "stroke-width": 3
                }
                
                lines["right_shoulder_connector"] = {
                    "x1": shoulder_center_x,
                    "y1": shoulder_center_y,
                    "x2": joints["right_shoulder"]["x"],
                    "y2": joints["right_shoulder"]["y"],
                    "stroke-width": 3
                }
            
            # 左臂: left_shoulder -> left_hand（分为上臂和前臂，中点插值）
            if "left_shoulder" in joints and "left_hand" in joints:
                elbow_x = (joints["left_shoulder"]["x"] + joints["left_hand"]["x"]) / 2
                elbow_y = (joints["left_shoulder"]["y"] + joints["left_hand"]["y"]) / 2
                
                lines["left_upper_arm"] = {
                    "x1": joints["left_shoulder"]["x"],
                    "y1": joints["left_shoulder"]["y"],
                    "x2": elbow_x,
                    "y2": elbow_y,
                    "stroke-width": 3
                }
                
                lines["left_forearm"] = {
                    "x1": elbow_x,
                    "y1": elbow_y,
                    "x2": joints["left_hand"]["x"],
                    "y2": joints["left_hand"]["y"],
                    "stroke-width": 3
                }
            
            # 右臂: right_shoulder -> right_hand
            if "right_shoulder" in joints and "right_hand" in joints:
                elbow_x = (joints["right_shoulder"]["x"] + joints["right_hand"]["x"]) / 2
                elbow_y = (joints["right_shoulder"]["y"] + joints["right_hand"]["y"]) / 2
                
                lines["right_upper_arm"] = {
                    "x1": joints["right_shoulder"]["x"],
                    "y1": joints["right_shoulder"]["y"],
                    "x2": elbow_x,
                    "y2": elbow_y,
                    "stroke-width": 3
                }
                
                lines["right_forearm"] = {
                    "x1": elbow_x,
                    "y1": elbow_y,
                    "x2": joints["right_hand"]["x"],
                    "y2": joints["right_hand"]["y"],
                    "stroke-width": 3
                }
            
            # 髋部连接器（左右）
            if "waist" in joints and "left_hip" in joints and "right_hip" in joints:
                lines["left_hip_connector"] = {
                    "x1": joints["waist"]["x"],
                    "y1": joints["waist"]["y"],
                    "x2": joints["left_hip"]["x"],
                    "y2": joints["left_hip"]["y"],
                    "stroke-width": 3
                }
                
                lines["right_hip_connector"] = {
                    "x1": joints["waist"]["x"],
                    "y1": joints["waist"]["y"],
                    "x2": joints["right_hip"]["x"],
                    "y2": joints["right_hip"]["y"],
                    "stroke-width": 3
                }
            
            # 左腿: left_hip -> left_foot（分为大腿和小腿）
            if "left_hip" in joints and "left_foot" in joints:
                knee_x = (joints["left_hip"]["x"] + joints["left_foot"]["x"]) / 2
                knee_y = (joints["left_hip"]["y"] + joints["left_foot"]["y"]) / 2
                
                lines["left_thigh"] = {
                    "x1": joints["left_hip"]["x"],
                    "y1": joints["left_hip"]["y"],
                    "x2": knee_x,
                    "y2": knee_y,
                    "stroke-width": 3
                }
                
                lines["left_calf"] = {
                    "x1": knee_x,
                    "y1": knee_y,
                    "x2": joints["left_foot"]["x"],
                    "y2": joints["left_foot"]["y"],
                    "stroke-width": 3
                }
            
            # 右腿: right_hip -> right_foot
            if "right_hip" in joints and "right_foot" in joints:
                knee_x = (joints["right_hip"]["x"] + joints["right_foot"]["x"]) / 2
                knee_y = (joints["right_hip"]["y"] + joints["right_foot"]["y"]) / 2
                
                lines["right_thigh"] = {
                    "x1": joints["right_hip"]["x"],
                    "y1": joints["right_hip"]["y"],
                    "x2": knee_x,
                    "y2": knee_y,
                    "stroke-width": 3
                }
                
                lines["right_calf"] = {
                    "x1": knee_x,
                    "y1": knee_y,
                    "x2": joints["right_foot"]["x"],
                    "y2": joints["right_foot"]["y"],
                    "stroke-width": 3
                }
        
        return lines
    
    def _render_converted_skeleton(self, pose: Dict[str, Any], color: str) -> List[str]:
        """
        渲染已转换的骨骼线段
        
        Args:
            pose: 转换后的线段数据
            color: 颜色
            
        Returns:
            SVG行列表
        """
        lines = []
        
        # 头部
        if "head" in pose:
            head = pose["head"]
            cx, cy, r = head.get("cx", 0), head.get("cy", 0), head.get("r", 20)
            lines.append(
                f'    <circle cx="{cx}" cy="{cy}" r="{r}" '
                f'stroke="{color}" fill="none" stroke-width="3"/>'
            )
        
        # 渲染所有线段（按照z-order）
        render_order = [
            "left_thigh", "left_calf", "right_thigh", "right_calf",
            "left_hip_connector", "right_hip_connector",
            "lower_torso", "upper_torso",
            "left_shoulder_connector", "right_shoulder_connector",
            "left_upper_arm", "left_forearm",
            "right_upper_arm", "right_forearm",
            "neck",
        ]
        
        for part_name in render_order:
            if part_name in pose:
                part = pose[part_name]
                x1 = part.get("x1", 0)
                y1 = part.get("y1", 0)
                x2 = part.get("x2", 0)
                y2 = part.get("y2", 0)
                width = part.get("stroke-width", 3)
                
                lines.append(
                    f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
                )
        
        return lines
    
    def _render_6dof_skeleton(self, pose: Dict[str, Any], color: str) -> List[str]:
        """渲染6DOF骨骼"""
        lines = []
        
        # 定义连接关系
        connections = [
            ("neck", "body"),
            ("body", "left_arm"),
            ("body", "right_arm"),
            ("body", "left_leg"),
            ("body", "right_leg"),
        ]
        
        for line_name in ["body", "left_arm", "right_arm", "left_leg", "right_leg"]:
            if line_name in pose:
                line_data = pose[line_name]
                x1 = line_data.get("x1", 0)
                y1 = line_data.get("y1", 0)
                x2 = line_data.get("x2", 0)
                y2 = line_data.get("y2", 0)
                width = line_data.get("stroke-width", 3)
                
                lines.append(
                    f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
                )
        
        return lines
    
    def _render_12dof_skeleton(self, pose: Dict[str, Any], color: str) -> List[str]:
        """渲染12DOF骨骼"""
        lines = []
        
        # 定义所有肢体部位
        parts = [
            "neck", "upper_torso", "lower_torso",
            "left_shoulder_connector", "right_shoulder_connector",
            "left_upper_arm", "left_forearm",
            "right_upper_arm", "right_forearm",
            "left_hip_connector", "right_hip_connector",
            "left_thigh", "left_calf",
            "right_thigh", "right_calf",
        ]
        
        # 按照z-order渲染（腿->躯干->手臂）
        render_order = [
            "left_thigh", "left_calf", "right_thigh", "right_calf",
            "left_hip_connector", "right_hip_connector",
            "lower_torso", "upper_torso",
            "left_shoulder_connector", "right_shoulder_connector",
            "left_upper_arm", "left_forearm",
            "right_upper_arm", "right_forearm",
            "neck",
        ]
        
        for part_name in render_order:
            if part_name in pose:
                part = pose[part_name]
                x1 = part.get("x1", 0)
                y1 = part.get("y1", 0)
                x2 = part.get("x2", 0)
                y2 = part.get("y2", 0)
                width = part.get("stroke-width", 3)
                
                lines.append(
                    f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
                )
        
        # 绘制关节点
        if "joints" in pose:
            for joint in pose["joints"]:
                cx = joint.get("cx", 0)
                cy = joint.get("cy", 0)
                r = joint.get("r", 3)
                
                lines.append(
                    f'    <circle cx="{cx}" cy="{cy}" r="{r}" '
                    f'fill="{color}"/>'
                )
        
        return lines
    
    def _escape_xml(self, text: str) -> str:
        """转义XML特殊字符"""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))
    
    def get_session_summary(self) -> Optional[Dict[str, Any]]:
        """
        获取当前会话的摘要信息
        
        Returns:
            摘要信息字典
        """
        if not self.enabled or not self.session_dir:
            return None
        
        return {
            "session_id": self.current_session_id,
            "session_dir": self.session_dir,
            "files": os.listdir(self.session_dir) if os.path.exists(self.session_dir) else []
        }
    
    def end_session(self):
        """结束当前会话"""
        if not self.enabled:
            return
        
        if self.current_session_id:
            logger.info(f"Debug session ended: {self.current_session_id}")
            logger.info(f"Debug files saved to: {self.session_dir}")
        
        self.current_session_id = None
        self.session_dir = None


# 全局单例
_debug_logger_instance: Optional[DebugLogger] = None


def get_debug_logger(enabled: bool = None, output_dir: str = None) -> DebugLogger:
    """
    获取全局调试记录器单例
    
    Args:
        enabled: 是否启用（仅首次初始化时有效）
        output_dir: 输出目录（仅首次初始化时有效）
        
    Returns:
        DebugLogger 实例
    """
    global _debug_logger_instance
    
    if _debug_logger_instance is None:
        from backend.config_loader import ConfigLoader
        
        # 从配置中读取默认值
        try:
            loader = ConfigLoader()
            loader.load()
            _enabled = enabled if enabled is not None else loader.get('debug.save_process_data', False)
            _output_dir = output_dir or loader.get('debug.process_data_dir', 'debug_logs')
        except Exception as e:
            # 如果配置加载失败，使用默认值
            logger.warning(f"Failed to load debug config, using defaults: {e}")
            _enabled = enabled if enabled is not None else False
            _output_dir = output_dir or 'debug_logs'
        
        _debug_logger_instance = DebugLogger(enabled=_enabled, output_dir=_output_dir)
    
    return _debug_logger_instance
