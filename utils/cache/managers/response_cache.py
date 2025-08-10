import hashlib
import json
from django.core.cache import cache
from datetime import datetime
from utils.cache.managers.versioned_cache import VersionedCacheManager


class ResponseCacheManager:
    @staticmethod
    def get_response_cache_key(request, view_name=None):
        """
        Generate base cache key for API response (without version)

        Args:
            request: HTTP request object
            view_name: Name of the view class

        Returns:
            str: Base cache key
        """
        key_data = {
            "path": request.path,
            "method": request.method,
            "query_params": request.GET.dict(),
            "view_name": view_name or request.resolver_match.view_name
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return f"response_{hashlib.md5(key_string.encode()).hexdigest()}"

    @staticmethod
    def get_versioned_cache_key(request, model_name, view_name=None):
        """
        Generate versioned cache key for API response
        
        Args:
            request: HTTP request object
            model_name (str): Name of the model
            view_name: Name of the view class
            
        Returns:
            str: Versioned cache key
        """
        base_key = ResponseCacheManager.get_response_cache_key(request, view_name)
        return VersionedCacheManager.get_versioned_key(base_key, model_name)

    @staticmethod
    def cache_versioned_response(request, model_name, response_data, status_code=200, timeout=300, view_name=None):
        """
        Cache API response with versioning support
        
        Args:
            request: HTTP request object
            model_name (str): Name of the model
            response_data: Response data to cache
            status_code (int): HTTP status code
            timeout (int): Cache timeout in seconds
            view_name: Name of the view class
            
        Returns:
            dict: Cached response data
        """
        base_key = ResponseCacheManager.get_response_cache_key(request, view_name)
        cached_response = {
            "data": response_data,
            "status_code": status_code,
            "cached_at": datetime.now().isoformat()
        }
        
        VersionedCacheManager.set_versioned_data(
            base_key=base_key,
            model_name=model_name,
            data=cached_response,
            timeout=timeout
        )
        return cached_response

    @staticmethod
    def get_versioned_cached_response(request, model_name, view_name=None):
        """
        Get versioned cached API response
        
        Args:
            request: HTTP request object
            model_name (str): Name of the model
            view_name: Name of the view class
            
        Returns:
            dict|None: Cached response data or None if not found
        """
        base_key = ResponseCacheManager.get_response_cache_key(request, view_name)
        return VersionedCacheManager.get_versioned_data(base_key, model_name)

    @staticmethod
    def cache_response(cache_key, response_data, status_code=200, timeout=300):
        """
        Legacy method - use cache_versioned_response instead
        
        Args:
            cache_key (str): Cache key
            response_data: Response data to cache
            status_code (int): HTTP status code
            timeout (int): Cache timeout in seconds

        Returns:
            dict: Cached response data
        """
        cached_response = {
            "data": response_data,
            "status_code": status_code,
            "cached_at": datetime.now().isoformat()
        }
        cache.set(cache_key, cached_response, timeout=timeout)
        return cached_response

    @staticmethod
    def get_cached_response(cache_key):
        """
        Legacy method - use get_versioned_cached_response instead
        
        Args:
            cache_key (str): Cache key

        Returns:
            dict|None: Cached response data or None
        """
        return cache.get(cache_key)

    @staticmethod
    def invalidate_response_cache(cache_key):
        """
        Legacy method - versioned cache handles invalidation automatically
        
        Args:
            cache_key (str): Cache key pattern to invalidate
        """
        keys = cache.keys(f"*{cache_key}*")
        if keys:
            cache.delete_many(keys)