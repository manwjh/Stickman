"""
Flask Application - AI Stick Figure Story Animator

3-Level Pipeline Architecture:
- Level 1: Story Analyzer
- Level 2: Animation Generator (Template-based or LLM batch)
- Level 3: Animation Optimizer

Author: Shenzhen Wang & AI
License: MIT
"""
import os
import sys
import logging
import time
from flask import Flask
from flask_cors import CORS

from backend.config_loader import load_config_to_env
from backend.utils.version import get_version
from backend.services.animation_pipeline import AnimationPipelineV2
from backend.rate_limiter import PerUserRateLimiter
from backend.cache_service import get_animation_cache
from backend.routes import register_main_routes, register_api_routes
from backend.routes.export import register_export_routes

# Load configuration into environment variables
try:
    config_loader = load_config_to_env('config.yml')
except FileNotFoundError as e:
    print("=" * 60)
    print("❌ Configuration file not found")
    print("=" * 60)
    print()
    print(str(e))
    print()
    print("Please ensure config.yml exists in the project root.")
    sys.exit(1)
except ValueError as e:
    print("=" * 60)
    print("❌ Configuration validation failed")
    print("=" * 60)
    print()
    print(str(e))
    print()
    print("=" * 60)
    print("🔧 Setup Instructions:")
    print("=" * 60)
    print()
    print("Step 1: Set API keys in environment")
    print("  $ source ./set_env.sh")
    print()
    print("Step 2: Start the application")
    print("  $ python3 app.py")
    print()
    print("Note: API keys must be set via set_env.sh before starting the app.")
    print()
    sys.exit(1)
except Exception as e:
    print("=" * 60)
    print("❌ Failed to load configuration")
    print("=" * 60)
    print()
    print(f"Error: {e}")
    print()
    sys.exit(1)

# Configure logging
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

# 配置 LiteLLM 日志级别为 ERROR，屏蔽 INFO 和 DEBUG 日志
logging.getLogger('LiteLLM').setLevel(logging.ERROR)
logging.getLogger('litellm').setLevel(logging.ERROR)


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    CORS(app)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_AS_ASCII'] = False
    
    # 注册 debug_logs 静态文件路由
    from flask import send_from_directory
    @app.route('/debug_logs/<path:filename>')
    def serve_debug_logs(filename):
        """提供 debug_logs 文件访问"""
        return send_from_directory('debug_logs', filename)
    
    rate_limiter = PerUserRateLimiter(
        requests_per_minute=int(os.getenv('RATE_LIMIT_PER_MINUTE', '20')),
        burst_size=int(os.getenv('RATE_LIMIT_BURST', '30'))
    )
    
    animation_cache = get_animation_cache()
    
    metrics = {
        'requests_total': 0,
        'requests_success': 0,
        'requests_failed': 0,
        'requests_cached': 0,
        'requests_rate_limited': 0,
        'total_latency': 0.0,
        'start_time': time.time()
    }
    
    should_initialize = os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or \
                       os.environ.get('WERKZEUG_RUN_MAIN') is None
    
    if not should_initialize:
        logger.info("⏭️  Skipping initialization in reloader monitor process")
        pipelines = {}
    else:
        logger.info("Initializing pipeline system...")
        pipelines = {
            '6dof': AnimationPipelineV2(dof_level='6dof', enable_optimization=True),
            '12dof': AnimationPipelineV2(dof_level='12dof', enable_optimization=True)
        }
        logger.info(f"✅ Pipelines initialized: {list(pipelines.keys())}")
    
    app.pipelines = pipelines
    app.rate_limiter = rate_limiter
    app.animation_cache = animation_cache
    app.metrics = metrics
    
    register_main_routes(app)
    register_api_routes(app)
    register_export_routes(app)
    
    @app.errorhandler(404)
    def not_found(error):
        from backend.utils.response import error_response
        return error_response('Endpoint not found', status_code=404)
    
    @app.errorhandler(500)
    def internal_error(error):
        from backend.utils.response import error_response
        logger.error(f"Internal server error: {error}", exc_info=True)
        return error_response('Internal server error', status_code=500)
    
    logger.info("Application initialized successfully")
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    version = get_version()
    
    print("=" * 60)
    print("🎬 AI Stick Figure Story Animator")
    print(f"   Version {version}")
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
    print("✨ Features:")
    print("   - 3-Level Pipeline Architecture")
    print("   - Template-based Generation (Walk, Wave, Bow)")
    print("   - Batch LLM Generation")
    print("   - Auto-fix Validation Errors")
    print("   - DOF Options: 6DOF / 12DOF")
    print("=" * 60)
    print()
    print("📄 Configuration Files:")
    print("   - config.yml (System Configuration)")
    print("   - llm_config.yml (API Tokens)")
    print()
    print("Detailed Configuration (Sensitive Info Masked):")
    print(config_loader.display())
    print()
    print("=" * 60)
    
    logger.info(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
