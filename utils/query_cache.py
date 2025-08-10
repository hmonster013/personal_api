from django.core.cache import cache
from django.db.models import QuerySet
from .versioned_cache import VersionedCacheManager
import hashlib
import json

class QueryCacheManager:
    @staticmethod
    def get_cache_key(model_name, filters=None, ordering=None):
        """
        Generate base cache key for queryset (without version)
        
        Args:
            model_name (str): Name of the model
            filters (dict): Query filters
            ordering (list): Ordering fields
            
        Returns:
            str: Base cache key
        """
        key_data = {
            "model": model_name,
            "filters": filters or {},
            "ordering": ordering or []
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return f"query_{hashlib.md5(key_string.encode()).hexdigest()}"
    
    @staticmethod
    def get_versioned_cache_key(model_name, filters=None, ordering=None):
        """
        Generate versioned cache key for queryset
        
        Args:
            model_name (str): Name of the model
            filters (dict): Query filters
            ordering (list): Ordering fields
            
        Returns:
            str: Versioned cache key
        """
        base_key = QueryCacheManager.get_cache_key(model_name, filters, ordering)
        return VersionedCacheManager.get_versioned_key(base_key, model_name)
    
    @staticmethod
    def cache_versioned_queryset(model_name, queryset, filters=None, ordering=None, timeout=300):
        """
        Cache queryset with versioning support
        
        Args:
            model_name (str): Name of the model
            queryset (QuerySet): Django queryset to cache
            filters (dict): Query filters used
            ordering (list): Ordering fields used
            timeout (int): Cache timeout in seconds
            
        Returns:
            list: Cached data as list of dictionaries
        """
        base_key = QueryCacheManager.get_cache_key(model_name, filters, ordering)
        data = list(queryset.values())
        
        # Store with versioned key
        VersionedCacheManager.set_versioned_data(
            base_key=base_key,
            model_name=model_name,
            data=data,
            timeout=timeout
        )
        return data
    
    @staticmethod
    def get_versioned_cached_queryset(model_name, filters=None, ordering=None):
        """
        Get versioned cached queryset
        
        Args:
            model_name (str): Name of the model
            filters (dict): Query filters
            ordering (list): Ordering fields
            
        Returns:
            list|None: Cached data or None if not found
        """
        base_key = QueryCacheManager.get_cache_key(model_name, filters, ordering)
        return VersionedCacheManager.get_versioned_data(base_key, model_name)
    
    # ================================
    # Legacy methods for backward compatibility
    # ================================
    @staticmethod
    def cache_queryset(cache_key, queryset, timeout=300):
        """
        Legacy method - use cache_versioned_queryset instead
        
        Args:
            cache_key (str): Cache key
            queryset (QuerySet): Django queryset
            timeout (int): Cache timeout
            
        Returns:
            list: Cached data
        """
        data = list(queryset.values())
        cache.set(cache_key, data, timeout=timeout)
        return data
    
    @staticmethod
    def get_cached_queryset(cache_key):
        """
        Legacy method - use get_versioned_cached_queryset instead
        
        Args:
            cache_key (str): Cache key
            
        Returns:
            list|None: Cached data or None
        """
        return cache.get(cache_key)
