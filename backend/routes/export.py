"""
Export Routes - GIF/Video Export API

Author: Shenzhen Wang & AI
License: MIT
"""
import logging
from flask import Blueprint, request, send_file, current_app
from backend.services.gif_exporter import create_gif_exporter
from backend.utils.response import success_response, error_response

logger = logging.getLogger(__name__)

bp = Blueprint('export', __name__, url_prefix='/api/export')


@bp.route('/gif', methods=['POST'])
def export_gif():
    """
    导出GIF动画
    
    Request Body:
    {
        "session_id": "20260119_092729_320",
        "fps": 30,           # optional
        "quality": 80,       # optional
        "optimize": true     # optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'session_id' not in data:
            return error_response('缺少 session_id 参数')
        
        session_id = data['session_id']
        fps = data.get('fps', 30)
        quality = data.get('quality', 80)
        optimize = data.get('optimize', True)
        
        # 验证参数
        if fps < 1 or fps > 60:
            return error_response('fps 必须在 1-60 之间')
        
        if quality < 1 or quality > 100:
            return error_response('quality 必须在 1-100 之间')
        
        # 创建GIF导出器
        exporter = create_gif_exporter()
        
        # 导出GIF
        result = exporter.export_from_session(
            session_id=session_id,
            fps=fps,
            quality=quality,
            optimize=optimize
        )
        
        if not result['success']:
            return error_response(
                result.get('error', 'GIF导出失败'),
                status_code=500
            )
        
        # 返回GIF文件
        return send_file(
            result['gif_path'],
            mimetype='image/gif',
            as_attachment=True,
            download_name=f'animation_{session_id}.gif'
        )
        
    except Exception as e:
        logger.error(f"GIF导出错误: {e}", exc_info=True)
        return error_response(str(e), status_code=500)


@bp.route('/check-support', methods=['GET'])
def check_export_support():
    """检查导出支持情况"""
    try:
        exporter = create_gif_exporter()
        methods = exporter.get_available_methods()
        
        return success_response(
            data={
                'gif_support': any(methods.values()),
                'methods': methods,
                'recommended': 'cairosvg' if methods.get('cairosvg') else 'svglib'
            },
            message='Export support checked'
        )
    except Exception as e:
        logger.error(f"检查导出支持失败: {e}", exc_info=True)
        return error_response(str(e), status_code=500)


def register_export_routes(app):
    """注册导出路由"""
    app.register_blueprint(bp)
