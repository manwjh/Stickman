"""
API Routes - REST API Endpoints

Author: Shenzhen Wang & AI
License: MIT
"""
import time
import logging
from flask import Blueprint, request, current_app
from backend.services.animation_pipeline import AnimationPipelineV2
from backend.utils.response import success_response, error_response
from backend.utils.version import get_version
from backend.security import sanitize_input, validate_content_type, validate_request_size
from backend.rate_limiter import PerUserRateLimiter
from backend.cache_service import get_animation_cache
import os

logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')

_pipelines = {}
_rate_limiter = None
_cache = None


def get_pipeline(dof_level: str = '12dof') -> AnimationPipelineV2:
    global _pipelines
    if dof_level not in _pipelines:
        logger.info(f"Creating pipeline for {dof_level}")
        _pipelines[dof_level] = AnimationPipelineV2(dof_level=dof_level, enable_optimization=True)
    return _pipelines[dof_level]


def get_rate_limiter() -> PerUserRateLimiter:
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = PerUserRateLimiter(max_requests=10, time_window=60)
    return _rate_limiter


def get_cache():
    global _cache
    if _cache is None:
        _cache = get_animation_cache()
    return _cache


@bp.route('/generate', methods=['POST'])
@validate_content_type('application/json')
@validate_request_size()
def generate_animation():
    start_time = time.time()
    data = request.get_json()
    
    if not data or 'story' not in data:
        return error_response('Missing story parameter')
    
    story = data['story'].strip()
    dof_level = data.get('dof_level', '12dof')
    use_cache = data.get('use_cache', True)
    
    if dof_level not in ['6dof', '12dof']:
        return error_response(f'Invalid dof_level: {dof_level}')
    
    try:
        story = sanitize_input(story)
    except ValueError as e:
        return error_response(str(e))
    
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    rate_limiter = current_app.rate_limiter if hasattr(current_app, 'rate_limiter') else get_rate_limiter()
    if not rate_limiter.try_acquire(client_ip):
        return error_response('Rate limit exceeded', status_code=429)
    
    cache = current_app.animation_cache if hasattr(current_app, 'animation_cache') else get_cache()
    cache_key = f"{story}:{dof_level}"
    
    if use_cache:
        cached_result = cache.get(cache_key)
        if cached_result:
            elapsed_ms = (time.time() - start_time) * 1000
            return success_response(
                data=cached_result['data'],
                message='Cached',
                cached=True,
                latency_ms=elapsed_ms
            )
    
    try:
        if hasattr(current_app, 'pipelines') and dof_level in current_app.pipelines:
            pipeline = current_app.pipelines[dof_level]
        else:
            pipeline = get_pipeline(dof_level)
        
        result = pipeline.generate(story=story)
        
        if result['success']:
            if use_cache:
                cache.put(cache_key, result)
            
            elapsed_ms = (time.time() - start_time) * 1000
            return success_response(
                data=result['data'],
                message='Success',
                cached=False,
                latency_ms=elapsed_ms,
                metadata=result['metadata']
            )
        else:
            return error_response(result.get('error', 'Failed'), status_code=500)
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return error_response(str(e), status_code=500)


@bp.route('/health', methods=['GET'])
def health_check():
    metrics = current_app.metrics if hasattr(current_app, 'metrics') else {}
    start_time = metrics.get('start_time', time.time())
    uptime_seconds = time.time() - start_time
    
    pipeline_status = {}
    if hasattr(current_app, 'pipelines'):
        for dof in ['6dof', '12dof']:
            if dof in current_app.pipelines:
                stats = current_app.pipelines[dof].get_stats()
                pipeline_status[dof] = {
                    'initialized': True,
                    'requests': stats['total_requests'],
                    'success_rate': stats['successful'] / stats['total_requests'] if stats['total_requests'] > 0 else 0
                }
            else:
                pipeline_status[dof] = {'initialized': False}
    
    return success_response(
        data={
            'status': 'healthy',
            'version': get_version(),
            'provider': os.getenv('LLM_PROVIDER', 'openai'),
            'uptime_seconds': round(uptime_seconds, 2),
            'architecture': '3-level-pipeline',
            'pipelines': pipeline_status
        },
        message='Service is healthy'
    )


@bp.route('/metrics', methods=['GET'])
def get_metrics():
    data = {'version': get_version(), 'pipelines': {}}
    for dof, p in _pipelines.items():
        data['pipelines'][dof] = p.get_stats()
    return success_response(data=data)


@bp.route('/version', methods=['GET'])
def version_info():
    return success_response(data={
        'version': get_version(),
        'name': 'Stickman Animator',
        'dof_options': ['6dof', '12dof'],
        'architecture': '3-level-pipeline',
        'features': [
            'Template-based generation',
            'Batch LLM generation',
            'Auto-fix validation errors',
            'Advanced interpolation'
        ]
    })


def register_api_routes(app):
    app.register_blueprint(bp)
