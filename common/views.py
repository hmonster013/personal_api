# common/views.py
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from configs import variable_systems
from configs.paginations import CustomPagination
from configs.variable_response import response_data
from utils.cache.mixins.query_cache_mixin import QueryCacheMixin
from utils.cache.mixins.response_cache_mixin import ResponseCacheMixin
from .models import Skills, Links, Contact
from .serializers import SkillsSerializer, LinksSerializer, ContactCreateSerializer
from .filters import SkillsFilter, LinksFilter
from helpers import helper
from django.utils.translation import gettext_lazy as _

class GetAllConfigView(ResponseCacheMixin, QueryCacheMixin, generics.GenericAPIView):
    response_cache_timeout = 3600  # 1 hour for config (rarely changes)

    def get(self, request, *args, **kwargs):
        try:
            res_data = {"baseLinks": variable_systems.BASE_LINK}
            return response_data(data=res_data)
        except Exception as ex:
            helper.print_log_error(func_name="get_all_config", error=ex)
            return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=None)

class SkillsListView(ResponseCacheMixin, QueryCacheMixin, generics.GenericAPIView):
    queryset = Skills.objects.all().order_by('id')
    serializer_class = SkillsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SkillsFilter
    pagination_class = CustomPagination
    page_size = 10
    response_cache_timeout = 1800  # 30 minutes for skills (rarely change)

    def get(self, request, *args, **kwargs):
        return self.handle_list_request(request)

class LinksListView(ResponseCacheMixin, QueryCacheMixin, generics.GenericAPIView):
    queryset = Links.objects.all().order_by('id')
    serializer_class = LinksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LinksFilter
    pagination_class = CustomPagination
    page_size = 1
    response_cache_timeout = 1800  # 30 minutes for links (rarely change)

    def get(self, request, *args, **kwargs):
        return self.handle_list_request(request)

class LinksDetailView(ResponseCacheMixin, QueryCacheMixin, generics.GenericAPIView):
    queryset = Links.objects.all().order_by('id')
    serializer_class = LinksSerializer
    response_cache_timeout = 1800  # 30 minutes for link details

    def get(self, request, id, *args, **kwargs):
        print(f"Lấy chi tiết link [{id}]")
        try:
            instance = self.get_queryset().get(id=id)
            serializer = self.serializer_class(instance)
            print(f"Lấy link thành công [{id}]")
            return response_data(data=serializer.data)
        except Links.DoesNotExist:
            print(f"Link ID [{id}] không hợp lệ")
            return response_data(
                status_code="ERROR",
                message=_("Link ID [{id}] không hợp lệ").format(id=id),
                status=status.HTTP_404_NOT_FOUND
            )

class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactCreateSerializer

    def post(self, request, *args, **kwargs):
        print("Tạo contact mới")
        try:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                contact = serializer.save()
                print(f"Tạo contact thành công [{contact.id}] - {contact.full_name}")
                return response_data(
                    message=_("Gửi tin nhắn thành công! Chúng tôi sẽ phản hồi sớm nhất có thể."),
                    data={"id": contact.id},
                    status=status.HTTP_201_CREATED
                )
            else:
                print(f"Lỗi validation: {serializer.errors}")
                return response_data(
                    status_code="ERROR",
                    message=_("Dữ liệu không hợp lệ"),
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            helper.print_log_error(func_name="ContactCreateView.post", error=ex)
            return response_data(
                status_code="ERROR",
                message=_("Có lỗi xảy ra khi gửi tin nhắn"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )