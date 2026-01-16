"""
Simple in-memory cache for query results
Reduces redundant LLM calls for similar questions
"""
import hashlib
from functools import lru_cache
from typing import Optional

# Simple dict cache (use Redis for production)
_query_cache = {}
MAX_CACHE_SIZE = 100

def get_cache_key(question: str, session_id: str) -> str:
    """Generate cache key from question and session"""
    combined = f"{session_id}:{question.lower().strip()}"
    return hashlib.md5(combined.encode()).hexdigest()

def get_cached_answer(question: str, session_id: str) -> Optional[dict]:
    """Retrieve cached answer if exists"""
    key = get_cache_key(question, session_id)
    return _query_cache.get(key)

def cache_answer(question: str, session_id: str, answer: dict):
    """Cache the answer"""
    key = get_cache_key(question, session_id)
    
    # Simple LRU: remove oldest if cache is full
    if len(_query_cache) >= MAX_CACHE_SIZE:
        oldest_key = next(iter(_query_cache))
        del _query_cache[oldest_key]
    
    _query_cache[key] = answer
    print(f"[INFO] Cached answer for query (cache size: {len(_query_cache)})")

def clear_cache():
    """Clear all cached queries"""
    _query_cache.clear()
    print("[INFO] Query cache cleared")
