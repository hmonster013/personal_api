from django.core.cache import cache
from django.db.models import QuerySet
import hashlib
import json

class QueryCacheManager:
    @staticmethod
    def get_cache_key(model_name, filters=None, ordering=None):
        """Generate cache key for queryset

        Args:
            model_name (str): Name of the model
            filters (dict, optional): Filters applied to the queryset. Defaults to None.
            ordering (list, optional): Ordering applied to the queryset. Defaults to None.

        Returns:
            str: Cache key
        """
        key_data = {
            "model": model_name,
            "filters": filters or {},
            "ordering": ordering or []
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return f"query_{hashlib.md5(key_string.encode()).hexdigest()}"
    
    @staticmethod
    def cache_queryset(cache_key, queryset, timeout=300):
        """Cache queryset

        Args:
            cache_key (str): Cache key
            queryset (QuerySet): Queryset to cache
            timeout (int, optional): Timeout in seconds. Defaults to 300.

        Returns:
            list: Cached data
        """
        data = list(queryset.values())
        cache.set(cache_key, data, timeout=timeout)
        return data
    
    @staticmethod
    def get_cached_queryset(cache_key):
        """Get cached queryset

        Args:
            cache_key (str): Cache key

        Returns:
            list: Cached data
        """
        return cache.get(cache_key)
    
    @staticmethod
    def invalidate_model_cache(model_name):
        """Invalidate cache for a model

        Args:
            model_name (str): Name of the model
        """
        cache.delete_many(cache.keys(f"*query_*{model_name}_*"))
