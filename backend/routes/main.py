"""
Main Routes - Static and UI Routes

Handles routes for serving static files and the main UI.

Author: Shenzhen Wang & AI
License: MIT
"""
from flask import Blueprint, render_template, send_from_directory
import os

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@bp.route('/favicon.ico')
def favicon():
    """Favicon route to prevent 404 errors"""
    from flask import current_app
    favicon_path = os.path.join(current_app.root_path, 'static')
    return send_from_directory(
        favicon_path,
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@bp.route('/manifest.json')
def manifest():
    """PWA manifest file"""
    from flask import current_app
    static_path = os.path.join(current_app.root_path, 'static')
    return send_from_directory(
        static_path,
        'manifest.json',
        mimetype='application/manifest+json'
    )


@bp.route('/sw.js')
def service_worker():
    """Service Worker for PWA"""
    from flask import current_app
    static_path = os.path.join(current_app.root_path, 'static')
    response = send_from_directory(
        static_path,
        'sw.js',
        mimetype='application/javascript'
    )
    # Service worker should not be cached
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def register_main_routes(app):
    """
    Register main routes with Flask app
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(bp)
