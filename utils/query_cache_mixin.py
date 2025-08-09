from configs.variable_response import response_data
from .query_cache import QueryCacheManager

class ListRequestMixin:
    """Base mixin for handling list requests with pagination"""

    def handle_list_request(self, request):
        """Handle list request with pagination support"""
        model_name = self.queryset.model.__name__.lower()
        print(f"Tìm kiếm {model_name}")

        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Tìm kiếm {model_name}, tổng số: [{result['paging']['total_rows']}]")
        return response_data(data=result)

class CacheQuerysetMixin(ListRequestMixin):
    cache_timeout = 300
    
    def handle_list_request(self, request):
        """Handle list request with caching support"""
        model_name = self.queryset.model.__name__.lower()
        print(f"Tìm kiếm {model_name}")

        if request.query_params.get("noPagination", "false").lower() == "true":
            cached_data = self.get_cached_query_set()
            return response_data(data={
                "data_list": cached_data,
                "paging": {
                    "total_rows": len(cached_data),
                    "page": 1,
                    "page_size": len(cached_data)
                }
            })

        # Paginated response
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Tìm kiếm {model_name}, tổng số: [{result['paging']['total_rows']}]")
        return response_data(data=result)

    def get_cached_query_set(self):
        """Get cached queryset

        Returns:
            list: Cached data
        """
        filters = self.request.GET.dict()
        model_name = self.queryset.model.__name__.lower()
        ordering = getattr(self, 'ordering', None)
        
        cache_key = QueryCacheManager.get_cache_key(
            model_name=model_name,
            filters=filters,
            ordering=ordering
        )
        
        cached_data = QueryCacheManager.get_cached_queryset(cache_key=cache_key)
        if cached_data is not None:
            print(f"Cache HIT for {model_name}: {cache_key}")
            return cached_data
        
        queryset = self.filter_queryset(self.get_queryset())
        cached_data = QueryCacheManager.cache_queryset(
            cache_key=cache_key,
            queryset=queryset,
            timeout=self.cache_timeout
        )
        print(f"Cache MISS for {model_name}: {cache_key}")
        return cached_data