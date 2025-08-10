from configs.variable_response import response_data
from .query_cache import QueryCacheManager
from .versioned_cache import VersionedCacheManager

class ListRequestMixin:
    """
    Base mixin for handling list requests with pagination
    
    This mixin provides basic functionality for handling list requests
    without any caching mechanism.
    """

    def handle_list_request(self, request):
        """
        Handle list request with pagination support
        
        Args:
            request: HTTP request object
            
        Returns:
            Response: Paginated response data
        """
        model_name = self.queryset.model.__name__.lower()
        print(f"Searching {model_name}")

        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Found {model_name}, total: [{result['paging']['total_rows']}]")
        return response_data(data=result)

class QueryCacheMixin(ListRequestMixin):
    """
    Enhanced query cache mixin with versioning support
    
    This mixin provides versioned caching for queryset data.
    When data changes, the version is incremented and cache is invalidated automatically.
    
    Attributes:
        cache_timeout (int): Cache timeout in seconds (default: 300)
    """
    cache_timeout = 300
    
    def handle_list_request(self, request):
        """
        Handle list request with versioned caching support
        
        For noPagination=true requests, uses versioned query cache.
        For paginated requests, uses regular flow (can be enhanced later).
        
        Args:
            request: HTTP request object
            
        Returns:
            Response: Cached or fresh response data
        """
        model_name = self.queryset.model.__name__.lower()
        print(f"Searching {model_name}")

        if request.query_params.get("noPagination", "false").lower() == "true":
            cached_data = self.get_versioned_cached_query_set()
            return response_data(data={
                "data_list": cached_data,
                "paging": {
                    "total_rows": len(cached_data),
                    "page": 1,
                    "page_size": len(cached_data)
                }
            })

        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Found {model_name}, total: [{result['paging']['total_rows']}]")
        return response_data(data=result)

    def get_versioned_cached_query_set(self):
        """
        Get versioned cached queryset
        
        This method first tries to get data from versioned cache.
        If cache miss, it queries the database and stores the result with version.
        
        Returns:
            list: Cached or fresh queryset data
        """
        filters = self.request.GET.dict()
        model_name = self.queryset.model.__name__.lower()
        ordering = getattr(self, 'ordering', None)
        
        cached_data = QueryCacheManager.get_versioned_cached_queryset(
            model_name=model_name,
            filters=filters,
            ordering=ordering
        )
        
        if cached_data is not None:
            version = VersionedCacheManager.get_current_version(model_name)
            print(f"Versioned query cache HIT for {model_name} v{version}")
            return cached_data
        
        queryset = self.filter_queryset(self.get_queryset())
        cached_data = QueryCacheManager.cache_versioned_queryset(
            model_name=model_name,
            queryset=queryset,
            filters=filters,
            ordering=ordering,
            timeout=self.cache_timeout
        )
        
        version = VersionedCacheManager.get_current_version(model_name)
        print(f"Versioned query cache MISS for {model_name} v{version}")
        return cached_data


