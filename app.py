"""
Flask Application - AI Stick Figure Story Animator

Provides RESTful API endpoints to receive user story descriptions
and generate stick figure animation data through LLM.

Main endpoints:
- GET  /              - Web interface
- POST /api/generate - Generate animation
- GET  /api/health   - Health check
- GET  /api/version  - Version information

Author: Shenzhen Wang & AI
License: MIT
Version: 0.1.0
"""
import os
import sys
import json
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Version information
__version__ = "0.1.0"

def get_version():
    """Get version from VERSION file or fallback to __version__"""
    try:
        version_file = Path(__file__).parent / 'VERSION'
        if version_file.exists():
            return version_file.read_text().strip()
    except Exception:
        pass
    return __version__

# First, load configuration into environment variables
from backend.config_loader import load_config_to_env

try:
    config_loader = load_config_to_env('config.yml', 'llm_config.yml')
except FileNotFoundError as e:
    print("=" * 60)
    print("❌ Configuration file not found")
    print("=" * 60)
    print()
    print(str(e))
    print()
    print("Please follow these steps:")
    print("1. Ensure config.yml exists (system configuration)")
    print("2. Copy LLM token configuration:")
    print("   cp llm_config.example.yml llm_config.yml")
    print("3. Edit llm_config.yml and fill in your API key")
    print("4. Run the program again")
    print()
    sys.exit(1)
except ValueError as e:
    print("=" * 60)
    print("❌ Configuration validation failed")
    print("=" * 60)
    print()
    print(str(e))
    print()
    print("Please check your llm_config.yml file")
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

from backend.llm_service import get_llm_service
from backend.animation_validator import validate_animation_data

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

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_AS_ASCII'] = False  # Support non-ASCII characters (Chinese, etc.)


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
            logger.warning(f"Validation warning: {str(ve)}")
            validated_data = animation_data
        
        return jsonify({
            'success': True,
            'data': validated_data,
            'message': 'Animation generated successfully'
        })
    
    except Exception as e:
        logger.error(f"Error generating animation: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating animation: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': get_version(),
        'provider': os.getenv('LLM_PROVIDER', 'openai')
    })


@app.route('/api/version', methods=['GET'])
def version_info():
    """Version information endpoint"""
    return jsonify({
        'version': get_version(),
        'name': 'AI Stick Figure Story Animator',
        'author': 'Shenzhen Wang & AI',
        'license': 'MIT'
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
