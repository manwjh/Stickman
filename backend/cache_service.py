"""
Cache Service

Implements LRU cache for animation results.

Author: Shenzhen Wang & AI
License: MIT
"""
import time
import hashlib
import json
from typing import Dict, Any, Optional
from collections import OrderedDict
import threading


class LRUCache:
    """
    Thread-safe LRU (Least Recently Used) cache
    
    Caches animation results with TTL (time-to-live) support.
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: int = 3600
    ):
        """
        Initialize LRU cache
        
        Args:
            max_size: Maximum number of items in cache
            ttl_seconds: Time-to-live for cached items (seconds)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict = OrderedDict()
        self.lock = threading.Lock()
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, story: str, **kwargs) -> str:
        """
        Generate cache key from story and parameters
        
        Args:
            story: Story description
            **kwargs: Additional parameters
            
        Returns:
            Cache key (SHA256 hash)
        """
        # Normalize story (lowercase, strip whitespace)
        normalized = story.strip().lower()
        
        # Include kwargs in key
        key_data = {
            'story': normalized,
            **kwargs
        }
        
        # Generate hash
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def get(self, story: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get cached result
        
        Args:
            story: Story description
            **kwargs: Additional parameters
            
        Returns:
            Cached result or None if not found/expired
        """
        key = self._make_key(story, **kwargs)
        
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            # Get cached item
            item = self.cache[key]
            
            # Check if expired
            if time.time() - item['timestamp'] > self.ttl_seconds:
                del self.cache[key]
                self.misses += 1
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.hits += 1
            
            return item['data']
    
    def put(self, story: str, data: Dict[str, Any], **kwargs):
        """
        Put result in cache
        
        Args:
            story: Story description
            data: Animation data to cache
            **kwargs: Additional parameters
        """
        key = self._make_key(story, **kwargs)
        
        with self.lock:
            # Add or update item
            self.cache[key] = {
                'data': data,
                'timestamp': time.time()
            }
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            
            # Evict oldest if over capacity
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
    
    def clear(self):
        """Clear all cached items"""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dict with cache stats
        """
        with self.lock:
            total = self.hits + self.misses
            hit_rate = self.hits / total if total > 0 else 0
            
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': hit_rate,
                'ttl_seconds': self.ttl_seconds
            }
    
    def cleanup_expired(self):
        """Remove all expired items"""
        now = time.time()
        
        with self.lock:
            expired_keys = [
                key for key, item in self.cache.items()
                if now - item['timestamp'] > self.ttl_seconds
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            return len(expired_keys)


# Global cache instance
_animation_cache: Optional[LRUCache] = None


def get_animation_cache() -> LRUCache:
    """Get or create animation cache singleton"""
    global _animation_cache
    if _animation_cache is None:
        _animation_cache = LRUCache(
            max_size=1000,
            ttl_seconds=3600  # 1 hour
        )
    return _animation_cache
