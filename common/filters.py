from django_filters import rest_framework as filters

from common.models import Links, Skills

class SkillsFilter(filters.FilterSet):
    kw = filters.CharFilter(method='filter_kw')

    class Meta:
        model = Skills
        fields = ['kw']

    def filter_kw(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

class LinksFilter(filters.FilterSet):
    kw = filters.CharFilter(method='filter_kw')

    class Meta:
        model = Links
        fields = ['kw']

    def filter_kw(self, queryset, name, value):
        return queryset.filter(name__icontains=value)