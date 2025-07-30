# common/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from configs import variable_systems
from configs.paginations import CustomPagination
from configs.variable_response import response_data
from utils import utils
from .models import Skills, Links, Contact
from .serializers import SkillsSerializer, LinksSerializer, ContactCreateSerializer
from .filters import SkillsFilter, LinksFilter
from helpers import helper
from django.utils.translation import gettext_lazy as _

@api_view(http_method_names=["GET"])
def get_all_config(request):
    try:
        res_data = {"baseLinks": variable_systems.BASE_LINK}
        return response_data(data=res_data)
    except Exception as ex:
        helper.print_log_error(func_name="get_all_config", error=ex)
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=None)

class SkillsListView(generics.GenericAPIView):
    queryset = Skills.objects.all().order_by('id')
    serializer_class = SkillsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SkillsFilter
    pagination_class = CustomPagination
    page_size = 10 

    def get(self, request, *args, **kwargs):
        print("Tìm kiếm skill")
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Tìm kiếm skill, tổng số: [{result['paging']['total_rows']}]")
        return response_data(data=result)

class LinksListView(generics.GenericAPIView):
    queryset = Links.objects.all().order_by('id')
    serializer_class = LinksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LinksFilter
    pagination_class = CustomPagination
    page_size = 1

    def get(self, request, *args, **kwargs):
        print("Tìm kiếm link")
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result = paginator.get_paginated_data(queryset, self.serializer_class, request)
        print(f"Tìm kiếm link, tổng số: [{result['paging']['total_rows']}]")
        return response_data(data=result)

class LinksDetailView(generics.GenericAPIView):
    queryset = Links.objects.all().order_by('id')
    serializer_class = LinksSerializer

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