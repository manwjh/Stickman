"""
Utility Functions - Common Helpers

This package contains utility functions used across the application.

Author: Shenzhen Wang & AI
License: MIT
"""

from .version import get_version
from .response import success_response, error_response

__all__ = ['get_version', 'success_response', 'error_response']
