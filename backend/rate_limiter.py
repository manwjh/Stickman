"""
Rate Limiter

Implements token bucket algorithm for rate limiting.

Author: Shenzhen Wang & AI
License: MIT
"""
import time
import threading
from typing import Optional


class RateLimiter:
    """
    Token bucket rate limiter
    
    Allows burst traffic while maintaining average rate limit.
    Thread-safe implementation.
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_size: Optional[int] = None
    ):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: Maximum requests per minute
            burst_size: Maximum burst size (defaults to requests_per_minute)
        """
        self.rate = requests_per_minute / 60.0  # requests per second
        self.burst_size = burst_size or requests_per_minute
        self.tokens = self.burst_size
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire a token, blocking if necessary
        
        Args:
            timeout: Maximum time to wait (None = wait forever)
            
        Returns:
            True if token acquired, False if timeout
        """
        deadline = None if timeout is None else time.time() + timeout
        
        while True:
            with self.lock:
                now = time.time()
                elapsed = now - self.last_update
                
                # Add tokens based on elapsed time
                self.tokens = min(
                    self.burst_size,
                    self.tokens + elapsed * self.rate
                )
                self.last_update = now
                
                # Try to consume a token
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
                
                # Check timeout
                if deadline is not None and now >= deadline:
                    return False
            
            # Wait a bit before retrying
            time.sleep(0.01)
    
    def try_acquire(self) -> bool:
        """
        Try to acquire a token without blocking
        
        Returns:
            True if token acquired, False otherwise
        """
        return self.acquire(timeout=0)
    
    def reset(self):
        """Reset the rate limiter to full capacity"""
        with self.lock:
            self.tokens = self.burst_size
            self.last_update = time.time()


class PerUserRateLimiter:
    """
    Per-user rate limiter
    
    Maintains separate rate limiters for each user.
    """
    
    def __init__(
        self,
        requests_per_minute: int = 20,
        burst_size: Optional[int] = None
    ):
        """
        Initialize per-user rate limiter
        
        Args:
            requests_per_minute: Maximum requests per minute per user
            burst_size: Maximum burst size per user
        """
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.limiters = {}
        self.lock = threading.Lock()
    
    def acquire(
        self,
        user_id: str,
        timeout: Optional[float] = None
    ) -> bool:
        """
        Acquire a token for a specific user
        
        Args:
            user_id: User identifier
            timeout: Maximum time to wait
            
        Returns:
            True if token acquired, False if timeout
        """
        with self.lock:
            if user_id not in self.limiters:
                self.limiters[user_id] = RateLimiter(
                    self.requests_per_minute,
                    self.burst_size
                )
        
        return self.limiters[user_id].acquire(timeout)
    
    def try_acquire(self, user_id: str) -> bool:
        """
        Try to acquire a token for a user without blocking
        
        Args:
            user_id: User identifier
            
        Returns:
            True if token acquired, False otherwise
        """
        return self.acquire(user_id, timeout=0)
    
    def reset(self, user_id: str):
        """Reset rate limiter for a specific user"""
        with self.lock:
            if user_id in self.limiters:
                self.limiters[user_id].reset()
    
    def reset_all(self):
        """Reset all user rate limiters"""
        with self.lock:
            for limiter in self.limiters.values():
                limiter.reset()
