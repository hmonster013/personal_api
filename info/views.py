# info/views.py
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend

from configs.paginations import CustomPagination
from configs.variable_response import response_data
from .models import Blogs, Experiences, Projects
from .serializers import BlogsSerializer, ExperiencesSerializer, ProjectsSerializer
from .filters import BlogsFilter, ExperiencesFilter, ProjectsFilter
from django.utils.translation import gettext_lazy as _

class BlogsListView(generics.GenericAPIView):
    queryset = Blogs.objects.all().order_by('id')
    serializer_class = BlogsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogsFilter
    pagination_class = CustomPagination
    page_size = 10

    def get(self, request, *args, **kwargs):
        print("Tìm kiếm blog")
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Tìm kiếm blog, tổng số: [{result['paging']['total_rows']}]")
        return response_data(data=result)

class BlogsDetailView(generics.GenericAPIView):
    queryset = Blogs.objects.all().order_by('id')
    serializer_class = BlogsSerializer

    def get(self, request, id, *args, **kwargs):
        print(f"Lấy chi tiết blog [{id}]")
        try:
            instance = self.get_queryset().get(id=id)
            serializer = self.serializer_class(instance)
            print(f"Lấy blog thành công [{id}]")
            return response_data(data=serializer.data)
        except Blogs.DoesNotExist:
            print(f"Blog ID [{id}] không hợp lệ")
            return response_data(
                status_code="ERROR",
                message=_("Blog ID [{id}] không hợp lệ").format(id=id),
                status=status.HTTP_404_NOT_FOUND
            )

class ExperiencesListView(generics.GenericAPIView):
    queryset = Experiences.objects.all().order_by('id')
    serializer_class = ExperiencesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExperiencesFilter
    pagination_class = CustomPagination
    page_size = 10

    def get(self, request, *args, **kwargs):
        print("Tìm kiếm experience")
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Tìm kiếm experience, tổng số: [{result['paging']['total_rows']}]")
        return response_data(data=result)

class ExperiencesDetailView(generics.GenericAPIView):
    queryset = Experiences.objects.all().order_by('id')
    serializer_class = ExperiencesSerializer

    def get(self, request, id, *args, **kwargs):
        print(f"Lấy chi tiết experience [{id}]")
        try:
            instance = self.get_queryset().get(id=id)
            serializer = self.serializer_class(instance)
            print(f"Lấy experience thành công [{id}]")
            return response_data(data=serializer.data)
        except Experiences.DoesNotExist:
            print(f"Experience ID [{id}] không hợp lệ")
            return response_data(
                status_code="ERROR",
                message=_("Experience ID [{id}] không hợp lệ").format(id=id),
                status=status.HTTP_404_NOT_FOUND
            )

class ProjectsListView(generics.GenericAPIView):
    queryset = Projects.objects.all().order_by('id')
    serializer_class = ProjectsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectsFilter
    pagination_class = CustomPagination
    page_size = 5

    def get(self, request, *args, **kwargs):
        print("Tìm kiếm project")
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Tìm kiếm project, tổng số: [{result['paging']['total_rows']}]")
        return response_data(data=result)

class ProjectsDetailView(generics.GenericAPIView):
    queryset = Projects.objects.all().order_by('id')
    serializer_class = ProjectsSerializer

    def get(self, request, id, *args, **kwargs):
        print(f"Lấy chi tiết project [{id}]")
        try:
            instance = self.get_queryset().get(id=id)
            serializer = self.serializer_class(instance)
            print(f"Lấy project thành công [{id}]")
            return response_data(data=serializer.data)
        except Projects.DoesNotExist:
            print(f"Project ID [{id}] không hợp lệ")
            return response_data(
                status_code="ERROR",
                message=_("Project ID [{id}] không hợp lệ").format(id=id),
                status=status.HTTP_404_NOT_FOUND
            )