"""
Response Utilities - Standardized API Response Format

Author: Shenzhen Wang & AI
License: MIT
"""
from typing import Any, Dict, Optional
from flask import jsonify


def success_response(
    data: Any = None,
    message: str = 'Success',
    **kwargs
) -> tuple:
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message: Success message
        **kwargs: Additional fields to include
        
    Returns:
        Tuple of (jsonify response, status_code)
    """
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    response.update(kwargs)
    
    return jsonify(response), 200


def error_response(
    message: str,
    status_code: int = 400,
    **kwargs
) -> tuple:
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        **kwargs: Additional fields to include
        
    Returns:
        Tuple of (jsonify response, status_code)
    """
    response = {
        'success': False,
        'message': message
    }
    
    response.update(kwargs)
    
    return jsonify(response), status_code
