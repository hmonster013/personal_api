from rest_framework import pagination
from rest_framework.response import Response

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

    def get_paginated_data(self, queryset, serializer_class, request):
        self.page_size = getattr(request, 'view', self).page_size if hasattr(request, 'view') and hasattr(request.view, 'page_size') else self.page_size
        if request.query_params.get('noPagination', 'false').lower() == 'true':
            serializer = serializer_class(queryset, many=True)
            return {
                "data_list": serializer.data,
                "paging": {
                    "total_rows": len(serializer.data),
                    "page": 1,
                    "page_size": len(serializer.data)
                }
            }
        page = self.paginate_queryset(queryset, request)
        serializer = serializer_class(page, many=True)
        return {
            "data_list": serializer.data,
            "paging": {
                "total_rows": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.page.paginator.per_page
            }
        }