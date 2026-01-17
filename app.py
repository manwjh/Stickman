"""
Flask 应用主程序 - AI 火柴人故事动画生成器

提供 RESTful API 接口，接收用户故事描述，
通过 LLM 生成火柴人动画数据。

主要端点:
- GET  /              - Web 界面
- POST /api/generate - 生成动画
- GET  /api/health   - 健康检查

Author: Your Name
License: MIT
"""
import os
import sys
import json
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# 首先加载配置到环境变量
from backend.config_loader import load_config_to_env

try:
    config_loader = load_config_to_env('config.yml', 'llm_config.yml')
except FileNotFoundError as e:
    print("=" * 60)
    print("❌ 配置文件不存在")
    print("=" * 60)
    print()
    print(str(e))
    print()
    print("请执行以下步骤:")
    print("1. 确保 config.yml 存在（系统配置）")
    print("2. 复制 LLM 令牌配置:")
    print("   cp llm_config.example.yml llm_config.yml")
    print("3. 编辑 llm_config.yml 文件，填入你的API密钥")
    print("4. 重新运行程序")
    print()
    sys.exit(1)
except ValueError as e:
    print("=" * 60)
    print("❌ 配置验证失败")
    print("=" * 60)
    print()
    print(str(e))
    print()
    print("请检查 llm_config.yml 文件中的配置")
    print()
    sys.exit(1)
except Exception as e:
    print("=" * 60)
    print("❌ 加载配置失败")
    print("=" * 60)
    print()
    print(f"错误: {e}")
    print()
    sys.exit(1)

from backend.llm_service import get_llm_service
from backend.animation_validator import validate_animation_data

# 配置日志
log_level = os.getenv('LOG_LEVEL', 'INFO')
log_format = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file = os.getenv('LOG_FILE', '')

logging.basicConfig(
    level=getattr(logging, log_level),
    format=log_format,
    handlers=[
        logging.StreamHandler(),
        *([logging.FileHandler(log_file)] if log_file else [])
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_AS_ASCII'] = False  # Support Chinese characters


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_animation():
    """
    Generate animation from story description
    
    Request JSON:
        {
            "story": "Story description in natural language"
        }
    
    Response JSON:
        {
            "success": true,
            "data": { animation_data },
            "message": "Success message"
        }
    """
    try:
        # Get story from request
        data = request.get_json()
        
        if not data or 'story' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing story parameter'
            }), 400
        
        story = data['story'].strip()
        
        if not story:
            return jsonify({
                'success': False,
                'message': 'Story cannot be empty'
            }), 400
        
        # Generate animation using LLM
        llm_service = get_llm_service()
        animation_data = llm_service.generate_animation(story)
        
        # Validate animation data
        try:
            validated_data = validate_animation_data(animation_data)
        except ValueError as ve:
            # If validation fails, return raw data with warning
            print(f"Validation warning: {str(ve)}")
            validated_data = animation_data
        
        return jsonify({
            'success': True,
            'data': validated_data,
            'message': 'Animation generated successfully'
        })
    
    except Exception as e:
        print(f"Error generating animation: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating animation: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'provider': os.getenv('LLM_PROVIDER', 'openai')
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("=" * 60)
    print("🎬 AI Stick Figure Story Animator")
    print("=" * 60)
    print(f"🌐 Server: http://{host}:{port}")
    
    provider = os.getenv('LLM_PROVIDER', 'openai')
    model_env_var = f"{provider.upper()}_MODEL"
    model = os.getenv(model_env_var, 'N/A')
    
    print(f"🤖 LLM Provider: {provider}")
    print(f"🎨 Model: {model}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"📊 Log Level: {log_level}")
    print("=" * 60)
    print()
    print("📄 配置文件:")
    print("   - config.yml (系统配置)")
    print("   - llm_config.yml (API令牌)")
    print()
    print("详细配置（敏感信息已隐藏）:")
    print(config_loader.display())
    print()
    print("=" * 60)
    
    logger.info(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
