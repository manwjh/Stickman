"""
Security Middleware

Implements security features for production deployment.

Author: Shenzhen Wang & AI
License: MIT
"""
import re
import hashlib
from typing import Optional
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)


class SecurityConfig:
    """Security configuration"""
    
    # Input sanitization patterns
    SQL_INJECTION_PATTERNS = [
        r"\bUNION\b.*\bSELECT\b",
        r"\bSELECT\b.*\bFROM\b",
        r"\bINSERT\b.*\bINTO\b",
        r"\bUPDATE\b.*\bSET\b",
        r"\bDELETE\b.*\bFROM\b",
        r"\bDROP\b.*\bTABLE\b",
        r"'OR'1'='1",
        r"';\s*--",
    ]
    
    # XSS patterns
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"onerror\s*=",
        r"onclick\s*=",
        r"onload\s*=",
    ]
    
    # Command injection patterns
    COMMAND_INJECTION_PATTERNS = [
        r"[;&|`$(){}[\]<>]",
        r"\.\./",
        r"/etc/passwd",
        r"/proc/",
    ]
    
    # Maximum content length (10MB)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    
    # Allowed origins (CORS)
    ALLOWED_ORIGINS = [
        'http://localhost:5000',
        'http://127.0.0.1:5000',
    ]


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        text: Input text
        
    Returns:
        Sanitized text
        
    Raises:
        ValueError: If malicious patterns detected
    """
    # Check for SQL injection
    for pattern in SecurityConfig.SQL_INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"SQL injection attempt detected: {pattern}")
            raise ValueError("Invalid input: potential SQL injection detected")
    
    # Check for XSS
    for pattern in SecurityConfig.XSS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"XSS attempt detected: {pattern}")
            raise ValueError("Invalid input: potential XSS detected")
    
    # Check for command injection
    for pattern in SecurityConfig.COMMAND_INJECTION_PATTERNS:
        if re.search(pattern, text):
            logger.warning(f"Command injection attempt detected: {pattern}")
            raise ValueError("Invalid input: potential command injection detected")
    
    return text


def validate_content_type(required_type: str = 'application/json'):
    """
    Decorator to validate request content type
    
    Args:
        required_type: Required content type
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            content_type = request.headers.get('Content-Type', '')
            
            if not content_type.startswith(required_type):
                logger.warning(f"Invalid content type: {content_type}")
                return jsonify({
                    'success': False,
                    'message': f'Content-Type must be {required_type}'
                }), 400
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


def validate_request_size():
    """Decorator to validate request size"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            content_length = request.content_length
            
            if content_length and content_length > SecurityConfig.MAX_CONTENT_LENGTH:
                logger.warning(f"Request too large: {content_length} bytes")
                return jsonify({
                    'success': False,
                    'message': 'Request body too large'
                }), 413
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


def require_api_key(f):
    """
    Decorator to require API key authentication
    
    Checks for X-API-Key header.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        import os
        
        # Get expected API key from environment
        expected_key = os.getenv('API_KEY')
        
        # If no API key configured, skip check (development mode)
        if not expected_key:
            return f(*args, **kwargs)
        
        # Get API key from request
        provided_key = request.headers.get('X-API-Key')
        
        if not provided_key:
            logger.warning("Missing API key")
            return jsonify({
                'success': False,
                'message': 'API key required'
            }), 401
        
        # Constant-time comparison to prevent timing attacks
        if not constant_time_compare(provided_key, expected_key):
            logger.warning("Invalid API key")
            return jsonify({
                'success': False,
                'message': 'Invalid API key'
            }), 403
        
        return f(*args, **kwargs)
    
    return wrapper


def constant_time_compare(a: str, b: str) -> bool:
    """
    Constant-time string comparison to prevent timing attacks
    
    Args:
        a: First string
        b: Second string
        
    Returns:
        True if strings are equal
    """
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    
    return result == 0


def hash_sensitive_data(data: str) -> str:
    """
    Hash sensitive data for logging
    
    Args:
        data: Sensitive data
        
    Returns:
        SHA256 hash (first 16 characters)
    """
    return hashlib.sha256(data.encode()).hexdigest()[:16]


def mask_api_key(api_key: str) -> str:
    """
    Mask API key for safe logging
    
    Args:
        api_key: API key
        
    Returns:
        Masked API key
    """
    if len(api_key) <= 8:
        return '***'
    
    return f"{api_key[:4]}...{api_key[-4:]}"
