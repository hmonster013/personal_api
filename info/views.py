# info/views.py
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend

from configs.paginations import CustomPagination
from configs.variable_response import response_data
from utils.query_cache_mixin import CacheQuerysetMixin, ListRequestMixin
from .models import Blogs, Experiences, Projects
from .serializers import BlogsSerializer, ExperiencesSerializer, ProjectsSerializer
from .filters import BlogsFilter, ExperiencesFilter, ProjectsFilter
from django.utils.translation import gettext_lazy as _

class BlogsListView(CacheQuerysetMixin, generics.GenericAPIView):
    queryset = Blogs.objects.all().order_by('id')
    serializer_class = BlogsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogsFilter
    pagination_class = CustomPagination
    page_size = 10
    cache_timeout = 600 # 10 minutes for blogs

    def get(self, request, *args, **kwargs):
        return self.handle_list_request(request)

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

class ExperiencesListView(CacheQuerysetMixin, generics.GenericAPIView):
    queryset = Experiences.objects.all().order_by('id')
    serializer_class = ExperiencesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExperiencesFilter
    pagination_class = CustomPagination
    page_size = 10
    cache_timeout = 900 # 15 minutes for experiences
    
    def get(self, request, *args, **kwargs):
        return self.handle_list_request(request)

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

class ProjectsListView(CacheQuerysetMixin, generics.GenericAPIView):
    queryset = Projects.objects.all().order_by('id')
    serializer_class = ProjectsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectsFilter
    pagination_class = CustomPagination
    page_size = 5

    def get(self, request, *args, **kwargs):
        return self.handle_list_request(request)

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