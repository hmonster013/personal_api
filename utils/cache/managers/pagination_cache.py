import hashlib
import json
from django.core.cache import cache
from utils.cache.managers.versioned_cache import VersionedCacheManager


class PaginationCacheManager:
    @staticmethod
    def get_cache_key(model_name, filters=None, ordering=None, page=1, page_size=12):
        """
        Generate base cache key for paginated data (without version)
        
        Args:
            model_name (str): Name of the model
            filters (dict): Query filters
            ordering (list): Ordering fields
            page (int): Page number
            page_size (int): Items per page
            
        Returns:
            str: Base cache key
        """
        key_data = {
            "model": model_name,
            "filters": filters or {},
            "ordering": ordering or [],
            "page": page,
            "page_size": page_size
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return f"pagination_{hashlib.md5(key_string.encode()).hexdigest()}"
    
    @staticmethod
    def get_versioned_cache_key(model_name, filters=None, ordering=None, page=1, page_size=12):
        """
        Generate versioned cache key for paginated data
        
        Args:
            model_name (str): Name of the model
            filters (dict): Query filters
            ordering (list): Ordering fields
            page (int): Page number
            page_size (int): Items per page
            
        Returns:
            str: Versioned cache key
        """
        base_key = PaginationCacheManager.get_cache_key(model_name, filters, ordering, page, page_size)
        return VersionedCacheManager.get_versioned_key(base_key, model_name)
    
    @staticmethod
    def cache_paginated_response(model_name, filters=None, ordering=None, page=1, page_size=12, response_data=None, timeout=300):
        """
        Cache paginated response with versioning support
        
        Args:
            model_name (str): Name of the model
            filters (dict): Query filters used
            ordering (list): Ordering fields used
            page (int): Page number
            page_size (int): Items per page
            response_data (dict): Response data to cache
            timeout (int): Cache timeout in seconds
            
        Returns:
            dict: Cached response data
        """
        base_key = PaginationCacheManager.get_cache_key(model_name, filters, ordering, page, page_size)
        
        VersionedCacheManager.set_versioned_data(
            base_key=base_key,
            model_name=model_name,
            data=response_data,
            timeout=timeout
        )
        return response_data
    
    @staticmethod
    def get_cached_paginated_response(model_name, filters=None, ordering=None, page=1, page_size=12):
        """
        Get versioned cached paginated response
        
        Args:
            model_name (str): Name of the model
            filters (dict): Query filters
            ordering (list): Ordering fields
            page (int): Page number
            page_size (int): Items per page
            
        Returns:
            dict|None: Cached response data or None if not found
        """
        base_key = PaginationCacheManager.get_cache_key(model_name, filters, ordering, page, page_size)
        return VersionedCacheManager.get_versioned_data(base_key, model_name)