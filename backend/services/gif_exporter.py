"""
GIF Exporter Service - Convert animation to GIF
使用已保存的SVG关键帧生成GIF动画

Author: Shenzhen Wang & AI
License: MIT
"""
import os
import logging
from pathlib import Path
from typing import Optional
from PIL import Image
import io

logger = logging.getLogger(__name__)


class GIFExporter:
    """GIF导出服务"""
    
    def __init__(self, debug_logs_dir: str = "debug_logs"):
        self.debug_logs_dir = debug_logs_dir
    
    def export_from_session(
        self,
        session_id: str,
        output_path: Optional[str] = None,
        fps: int = 30,
        quality: int = 80,
        optimize: bool = True
    ) -> dict:
        """
        从debug session导出GIF
        
        Args:
            session_id: debug session ID
            output_path: 输出路径，默认为session目录下的animation.gif
            fps: 帧率
            quality: 质量 (1-100)
            optimize: 是否优化文件大小
            
        Returns:
            dict: {
                'success': bool,
                'gif_path': str,
                'file_size': int,
                'frame_count': int,
                'duration_ms': int
            }
        """
        try:
            session_dir = Path(self.debug_logs_dir) / session_id
            svg_dir = session_dir / "keyframe_svgs"
            
            if not svg_dir.exists():
                raise FileNotFoundError(f"SVG目录不存在: {svg_dir}")
            
            # 获取所有SVG文件
            svg_files = sorted(svg_dir.glob("keyframe_*.svg"))
            
            if not svg_files:
                raise FileNotFoundError(f"没有找到SVG文件: {svg_dir}")
            
            logger.info(f"找到 {len(svg_files)} 个SVG文件")
            
            # 尝试使用cairosvg转换
            try:
                frames = self._convert_svgs_with_cairo(svg_files)
            except ImportError:
                # 降级到其他方案
                logger.warning("cairosvg未安装，尝试使用其他方案")
                frames = self._convert_svgs_with_pillow(svg_files)
            
            # 生成GIF
            if output_path is None:
                output_path = session_dir / "animation.gif"
            else:
                output_path = Path(output_path)
            
            duration_ms = int(1000 / fps)
            
            # 保存GIF
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=duration_ms,
                loop=0,
                optimize=optimize,
                quality=quality
            )
            
            file_size = output_path.stat().st_size
            total_duration = len(frames) * duration_ms
            
            logger.info(
                f"GIF导出成功: {output_path} "
                f"({len(frames)}帧, {file_size/1024:.1f}KB)"
            )
            
            return {
                'success': True,
                'gif_path': str(output_path),
                'file_size': file_size,
                'frame_count': len(frames),
                'duration_ms': total_duration
            }
            
        except Exception as e:
            logger.error(f"GIF导出失败: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    def _convert_svgs_with_cairo(self, svg_files: list) -> list:
        """使用cairosvg转换SVG到PNG"""
        import cairosvg
        
        frames = []
        for svg_file in svg_files:
            # SVG → PNG bytes
            png_bytes = cairosvg.svg2png(
                url=str(svg_file),
                output_width=800,
                output_height=600
            )
            
            # PNG bytes → PIL Image
            img = Image.open(io.BytesIO(png_bytes))
            
            # 转换为RGB模式（GIF需要）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            frames.append(img)
        
        return frames
    
    def _convert_svgs_with_pillow(self, svg_files: list) -> list:
        """使用Pillow直接加载SVG（需要安装svglib）"""
        try:
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPM
            
            frames = []
            for svg_file in svg_files:
                # SVG → ReportLab Drawing
                drawing = svg2rlg(str(svg_file))
                
                # Drawing → PIL Image
                png_bytes = renderPM.drawToString(drawing, fmt='PNG')
                img = Image.open(io.BytesIO(png_bytes))
                
                # 调整大小
                img = img.resize((800, 600), Image.Resampling.LANCZOS)
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                frames.append(img)
            
            return frames
            
        except ImportError:
            raise ImportError(
                "需要安装 cairosvg 或 svglib: "
                "pip install cairosvg 或 pip install svglib reportlab"
            )
    
    def get_available_methods(self) -> dict:
        """检查可用的转换方法"""
        methods = {}
        
        try:
            import cairosvg
            methods['cairosvg'] = True
        except ImportError:
            methods['cairosvg'] = False
        
        try:
            from svglib.svglib import svg2rlg
            methods['svglib'] = True
        except ImportError:
            methods['svglib'] = False
        
        return methods


def create_gif_exporter() -> GIFExporter:
    """创建GIF导出器实例"""
    return GIFExporter()
