"""
Routes - API Endpoints

This package contains route handlers for the Flask application.

Author: Shenzhen Wang & AI
License: MIT
"""

from .main import register_main_routes
from .api import register_api_routes

__all__ = ['register_main_routes', 'register_api_routes']
