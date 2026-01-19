"""
Unit Tests for Rate Limiter and Cache

Tests rate limiting and caching functionality.

Author: Shenzhen Wang & AI
License: MIT
"""
import pytest
import time
from backend.rate_limiter import RateLimiter, PerUserRateLimiter
from backend.cache_service import LRUCache, get_animation_cache


class TestRateLimiter:
    """Test rate limiter functionality"""
    
    def test_create_rate_limiter(self):
        """Test creating a rate limiter"""
        limiter = RateLimiter(requests_per_minute=60)
        assert limiter.rate == 1.0  # 60/60 = 1 per second
        assert limiter.burst_size == 60
    
    def test_acquire_token(self):
        """Test acquiring tokens"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=10)
        
        # Should be able to acquire
        assert limiter.acquire(timeout=1) == True
    
    def test_try_acquire(self):
        """Test non-blocking token acquisition"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=2)
        
        # First two should succeed
        assert limiter.try_acquire() == True
        assert limiter.try_acquire() == True
        
        # Third should fail (burst exhausted)
        assert limiter.try_acquire() == False
    
    def test_token_replenishment(self):
        """Test that tokens replenish over time"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=1)
        
        # Exhaust tokens
        assert limiter.try_acquire() == True
        assert limiter.try_acquire() == False
        
        # Wait for replenishment
        time.sleep(1.1)
        
        # Should be able to acquire again
        assert limiter.try_acquire() == True
    
    def test_reset(self):
        """Test resetting rate limiter"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=2)
        
        # Exhaust tokens
        limiter.try_acquire()
        limiter.try_acquire()
        assert limiter.try_acquire() == False
        
        # Reset
        limiter.reset()
        
        # Should work again
        assert limiter.try_acquire() == True


class TestPerUserRateLimiter:
    """Test per-user rate limiter"""
    
    def test_create_per_user_limiter(self):
        """Test creating per-user rate limiter"""
        limiter = PerUserRateLimiter(requests_per_minute=20)
        assert limiter.requests_per_minute == 20
    
    def test_different_users_independent(self):
        """Test that different users have independent limits"""
        limiter = PerUserRateLimiter(requests_per_minute=60, burst_size=2)
        
        # User 1 exhausts tokens
        assert limiter.try_acquire("user1") == True
        assert limiter.try_acquire("user1") == True
        assert limiter.try_acquire("user1") == False
        
        # User 2 should still have tokens
        assert limiter.try_acquire("user2") == True
    
    def test_reset_user(self):
        """Test resetting specific user"""
        limiter = PerUserRateLimiter(requests_per_minute=60, burst_size=1)
        
        # User exhausts tokens
        assert limiter.try_acquire("user1") == True
        assert limiter.try_acquire("user1") == False
        
        # Reset user
        limiter.reset("user1")
        
        # Should work again
        assert limiter.try_acquire("user1") == True


class TestLRUCache:
    """Test LRU cache functionality"""
    
    def test_create_cache(self):
        """Test creating a cache"""
        cache = LRUCache(max_size=100, ttl_seconds=60)
        assert cache.max_size == 100
        assert cache.ttl_seconds == 60
    
    def test_put_and_get(self):
        """Test putting and getting items"""
        cache = LRUCache(max_size=10, ttl_seconds=60)
        
        data = {"test": "data"}
        cache.put("story1", data)
        
        result = cache.get("story1")
        assert result == data
    
    def test_cache_miss(self):
        """Test cache miss returns None"""
        cache = LRUCache()
        
        result = cache.get("nonexistent")
        assert result is None
    
    def test_ttl_expiration(self):
        """Test that items expire after TTL"""
        cache = LRUCache(max_size=10, ttl_seconds=1)
        
        cache.put("story1", {"test": "data"})
        
        # Should exist immediately
        assert cache.get("story1") is not None
        
        # Wait for expiration
        time.sleep(1.5)
        
        # Should be expired
        assert cache.get("story1") is None
    
    def test_lru_eviction(self):
        """Test that least recently used items are evicted"""
        cache = LRUCache(max_size=3, ttl_seconds=60)
        
        # Fill cache
        cache.put("story1", {"data": 1})
        cache.put("story2", {"data": 2})
        cache.put("story3", {"data": 3})
        
        # Access story1 to make it recently used
        cache.get("story1")
        
        # Add new item (should evict story2, the LRU)
        cache.put("story4", {"data": 4})
        
        # story2 should be evicted
        assert cache.get("story2") is None
        # Others should still exist
        assert cache.get("story1") is not None
        assert cache.get("story3") is not None
        assert cache.get("story4") is not None
    
    def test_cache_statistics(self):
        """Test cache statistics tracking"""
        cache = LRUCache(max_size=10, ttl_seconds=60)
        
        cache.put("story1", {"data": 1})
        
        # Hit
        cache.get("story1")
        
        # Miss
        cache.get("story2")
        
        stats = cache.get_stats()
        
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['size'] == 1
        assert 0 < stats['hit_rate'] < 1
    
    def test_clear_cache(self):
        """Test clearing cache"""
        cache = LRUCache()
        
        cache.put("story1", {"data": 1})
        cache.put("story2", {"data": 2})
        
        cache.clear()
        
        assert cache.get("story1") is None
        assert cache.get("story2") is None
        
        stats = cache.get_stats()
        assert stats['size'] == 0
        assert stats['hits'] == 0
    
    def test_cleanup_expired(self):
        """Test cleaning up expired items"""
        cache = LRUCache(max_size=10, ttl_seconds=1)
        
        cache.put("story1", {"data": 1})
        cache.put("story2", {"data": 2})
        
        # Wait for expiration
        time.sleep(1.5)
        
        # Cleanup
        expired_count = cache.cleanup_expired()
        
        assert expired_count == 2
        assert cache.get_stats()['size'] == 0


class TestCacheSingleton:
    """Test cache singleton"""
    
    def test_get_animation_cache_singleton(self):
        """Test that get_animation_cache returns singleton"""
        cache1 = get_animation_cache()
        cache2 = get_animation_cache()
        
        assert cache1 is cache2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
