from configs.variable_response import response_data
from utils.cache.managers.query_cache import QueryCacheManager
from utils.cache.managers.versioned_cache import VersionedCacheManager

class ListRequestMixin:
    """Base mixin for handling list requests with pagination"""

    def handle_list_request(self, request):
        """Handle list request with pagination support"""
        model_name = self.queryset.model.__name__.lower()
        print(f"Searching {model_name}")

        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        
        # Use cached pagination method
        cache_timeout = getattr(self, 'cache_timeout', 300)
        result = paginator.get_paginated_data_with_cache(
            queryset, self.serializer_class, request, self, cache_timeout
        )
            
        print(f"Found {model_name}, total: [{result['paging']['total_rows']}]")
        return response_data(data=result)

class QueryCacheMixin(ListRequestMixin):
    """Enhanced query cache mixin with versioning support"""
    cache_timeout = 300
    
    def handle_list_request(self, request):
        """Handle list request with versioned caching support"""
        model_name = self.queryset.model.__name__.lower()
        print(f"Searching {model_name}")

        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        
        # Use cached pagination method
        cache_timeout = getattr(self, 'cache_timeout', 300)
        result = paginator.get_paginated_data_with_cache(
            queryset, self.serializer_class, request, self, cache_timeout
        )
        
        print(f"Found {model_name}, total: [{result['paging']['total_rows']}]")
        return response_data(data=result)


