from rest_framework import pagination
from rest_framework.response import Response
from utils.cache.managers.versioned_cache import VersionedCacheManager
from utils.cache.managers.pagination_cache import PaginationCacheManager

class CustomPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'pageSize'
    max_page_size = 10000

    def paginate_queryset(self, queryset, request, view=None):
        # Ưu tiên page_size từ view nếu có
        self.page_size = getattr(view, 'page_size', self.page_size)
        if request.query_params.get('noPagination', 'false').lower() == 'true':
            return None
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            "data_list": data,
            "paging": {
                "total_rows": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.page.paginator.per_page
            }
        })

    def get_paginated_data_with_cache(self, queryset, serializer_class, request, view=None, cache_timeout=300):
        """
        Get paginated data with caching support
        
        Args:
            queryset: Django queryset
            serializer_class: Serializer class
            request: HTTP request
            view: View instance
            cache_timeout: Cache timeout in seconds
            
        Returns:
            dict: Paginated response data
        """
        model_name = queryset.model.__name__.lower()
        filters = request.GET.dict()
        ordering = getattr(view, 'ordering', None)
        
        # Handle noPagination case
        if request.query_params.get('noPagination', 'false').lower() == 'true':
            # Use existing query cache for noPagination
            from utils.cache.managers.query_cache import QueryCacheManager
            
            cached_data = QueryCacheManager.get_versioned_cached_queryset(
                model_name=model_name,
                filters=filters,
                ordering=ordering
            )
            
            if cached_data is not None:
                version = VersionedCacheManager.get_current_version(model_name)
                print(f"Query cache HIT for {model_name} noPagination v{version}")
                return {
                    "data_list": cached_data,
                    "paging": {
                        "total_rows": len(cached_data),
                        "page": 1,
                        "page_size": len(cached_data)
                    }
                }
            
            # Cache miss - serialize and cache
            serializer = serializer_class(queryset, many=True)
            data = serializer.data
            
            QueryCacheManager.cache_versioned_queryset(
                model_name=model_name,
                queryset=queryset,
                filters=filters,
                ordering=ordering,
                timeout=cache_timeout
            )
            
            version = VersionedCacheManager.get_current_version(model_name)
            print(f"Query cache MISS for {model_name} noPagination v{version}")
            
            return {
                "data_list": data,
                "paging": {
                    "total_rows": len(data),
                    "page": 1,
                    "page_size": len(data)
                }
            }
        
        # Handle pagination case
        self.page_size = getattr(view, 'page_size', self.page_size)
        page_number = request.query_params.get('page', 1)
        
        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            page_number = 1
            
        # Try pagination cache first
        cached_response = PaginationCacheManager.get_cached_paginated_response(
            model_name=model_name,
            filters=filters,
            ordering=ordering,
            page=page_number,
            page_size=self.page_size
        )
        
        if cached_response:
            version = VersionedCacheManager.get_current_version(model_name)
            print(f"Pagination cache HIT for {model_name} page {page_number} v{version}")
            return cached_response
        
        # Cache miss - paginate and serialize
        page = self.paginate_queryset(queryset, request, view)
        if page is None:
            # Fallback if pagination fails
            serializer = serializer_class(queryset, many=True)
            return {
                "data_list": serializer.data,
                "paging": {
                    "total_rows": len(serializer.data),
                    "page": 1,
                    "page_size": len(serializer.data)
                }
            }
        
        serializer = serializer_class(page, many=True)
        response_data = {
            "data_list": serializer.data,
            "paging": {
                "total_rows": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.page.paginator.per_page
            }
        }
        
        # Cache the paginated response
        PaginationCacheManager.cache_paginated_response(
            model_name=model_name,
            filters=filters,
            ordering=ordering,
            page=page_number,
            page_size=self.page_size,
            response_data=response_data,
            timeout=cache_timeout
        )
        
        version = VersionedCacheManager.get_current_version(model_name)
        print(f"Pagination cache MISS for {model_name} page {page_number} v{version}")
        
        return response_data
