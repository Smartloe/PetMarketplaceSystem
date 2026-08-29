"""
Cache utility functions for common caching patterns.

Provides decorators and helpers for caching querysets, API responses,
and computed data to improve performance.
"""

import hashlib
import json
import logging
from functools import wraps
from typing import Any, Callable, Optional, Union

from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

# Cache key prefixes
CACHE_PREFIX_COMMODITY = 'commodity'
CACHE_PREFIX_CATEGORY = 'category'
CACHE_PREFIX_USER = 'user'
CACHE_PREFIX_ORDER = 'order'
CACHE_PREFIX_STATS = 'stats'

# Default cache timeouts (in seconds)
CACHE_TIMEOUT_SHORT = 5 * 60  # 5 minutes
CACHE_TIMEOUT_MEDIUM = 30 * 60  # 30 minutes
CACHE_TIMEOUT_LONG = 60 * 60  # 1 hour
CACHE_TIMEOUT_DAY = 24 * 60 * 60  # 24 hours


def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate a deterministic cache key from prefix and arguments.

    Args:
        prefix: Cache key prefix (e.g., 'commodity', 'user')
        *args: Positional arguments to include in key
        **kwargs: Keyword arguments to include in key

    Returns:
        A unique cache key string
    """
    # Create a string representation of all arguments
    key_parts = [str(prefix)]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))

    # Create a hash of the key parts for consistent length
    key_string = ':'.join(key_parts)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()[:12]

    return f"{prefix}:{key_hash}"


def cache_response(
    prefix: str,
    timeout: int = CACHE_TIMEOUT_MEDIUM,
    key_func: Optional[Callable] = None,
):
    """
    Decorator to cache API view responses.

    Args:
        prefix: Cache key prefix
        timeout: Cache timeout in seconds
        key_func: Optional function to generate custom cache key

    Example:
        @cache_response('commodity_list', timeout=300)
        def list(self, request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(request, *args, **kwargs)
            else:
                # Default key based on user, path, and query params
                user_id = request.user.id if request.user.is_authenticated else 'anon'
                query_params = request.GET.urlencode()
                cache_key = generate_cache_key(
                    prefix,
                    user_id,
                    request.path,
                    query_params,
                )

            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_response

            # Execute view and cache response
            logger.debug(f"Cache miss: {cache_key}")
            response = view_func(self, request, *args, **kwargs)

            # Only cache successful responses
            if response.status_code == 200:
                cache.set(cache_key, response, timeout)

            return response
        return wrapper
    return decorator


def cache_queryset(
    prefix: str,
    timeout: int = CACHE_TIMEOUT_MEDIUM,
    key_func: Optional[Callable] = None,
):
    """
    Decorator to cache queryset results.

    Args:
        prefix: Cache key prefix
        timeout: Cache timeout in seconds
        key_func: Optional function to generate custom cache key

    Example:
        @cache_queryset('commodity_list')
        def get_queryset(self):
            ...
    """
    def decorator(queryset_func):
        @wraps(queryset_func)
        def wrapper(self, *args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(self, *args, **kwargs)
            else:
                # Default key based on view and arguments
                cache_key = generate_cache_key(
                    prefix,
                    self.__class__.__name__,
                    *args,
                    **kwargs,
                )

            # Try to get from cache
            cached_queryset = cache.get(cache_key)
            if cached_queryset is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_queryset

            # Execute queryset function and cache result
            logger.debug(f"Cache miss: {cache_key}")
            queryset = queryset_func(self, *args, **kwargs)

            # Convert queryset to list for caching (querysets are lazy)
            result_list = list(queryset)
            cache.set(cache_key, result_list, timeout)

            return result_list
        return wrapper
    return decorator


def invalidate_cache(prefix: str, *args, **kwargs) -> None:
    """
    Invalidate cache entries matching the given prefix and arguments.

    Args:
        prefix: Cache key prefix
        *args: Arguments used to generate cache key
        **kwargs: Keyword arguments used to generate cache key
    """
    cache_key = generate_cache_key(prefix, *args, **kwargs)
    cache.delete(cache_key)
    logger.debug(f"Cache invalidated: {cache_key}")


def invalidate_pattern(pattern: str) -> None:
    """
    Invalidate all cache entries matching a pattern.

    Note: This only works with cache backends that support pattern matching
    (e.g., Redis, Memcached). For LocMemCache, this is a no-op.

    Args:
        pattern: Cache key pattern to match (e.g., 'commodity:*')
    """
    try:
        # Try to use cache.clear with pattern if supported
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern(pattern)
            logger.debug(f"Cache pattern invalidated: {pattern}")
        else:
            logger.warning(f"Cache backend does not support pattern deletion: {pattern}")
    except Exception as e:
        logger.error(f"Failed to invalidate cache pattern {pattern}: {e}")


# Predefined cache functions for common use cases
def get_cached_commodity_list(category_id: Optional[int] = None, page: int = 1):
    """
    Get cached commodity list.

    Args:
        category_id: Optional category filter
        page: Page number for pagination

    Returns:
        Cached commodity list or None
    """
    cache_key = generate_cache_key(
        CACHE_PREFIX_COMMODITY,
        'list',
        category_id=category_id,
        page=page,
    )
    return cache.get(cache_key)


def set_cached_commodity_list(data: Any, category_id: Optional[int] = None, page: int = 1):
    """
    Cache commodity list.

    Args:
        data: Data to cache
        category_id: Optional category filter
        page: Page number for pagination
    """
    cache_key = generate_cache_key(
        CACHE_PREFIX_COMMODITY,
        'list',
        category_id=category_id,
        page=page,
    )
    cache.set(cache_key, data, CACHE_TIMEOUT_SHORT)


def invalidate_commodity_cache(commodity_id: Optional[int] = None):
    """
    Invalidate commodity-related caches.

    Args:
        commodity_id: Optional specific commodity ID to invalidate
    """
    if commodity_id:
        invalidate_cache(CACHE_PREFIX_COMMODITY, commodity_id)
    # Invalidate list caches
    invalidate_pattern(f"{CACHE_PREFIX_COMMODITY}:*")


def get_cached_user_profile(user_id: int):
    """
    Get cached user profile.

    Args:
        user_id: User ID

    Returns:
        Cached user profile or None
    """
    cache_key = generate_cache_key(CACHE_PREFIX_USER, 'profile', user_id)
    return cache.get(cache_key)


def set_cached_user_profile(user_id: int, data: Any):
    """
    Cache user profile.

    Args:
        user_id: User ID
        data: Data to cache
    """
    cache_key = generate_cache_key(CACHE_PREFIX_USER, 'profile', user_id)
    cache.set(cache_key, data, CACHE_TIMEOUT_MEDIUM)


def invalidate_user_cache(user_id: int):
    """
    Invalidate user-related caches.

    Args:
        user_id: User ID
    """
    invalidate_cache(CACHE_PREFIX_USER, 'profile', user_id)
    invalidate_pattern(f"{CACHE_PREFIX_USER}:*{user_id}*")