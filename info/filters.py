from django_filters import rest_framework as filters
from info.models import Blogs, Experiences, Projects


class BlogsFilter(filters.FilterSet):
    kw = filters.CharFilter(method='filter_kw')

    class Meta:
        model = Blogs
        fields = ['kw']

    def filter_kw(self, queryset, name, value):
        return queryset.filter(title__icontains=value) | \
            queryset.filter(content__icontains=value) | \
            queryset.filter(description__icontains=value)

class ExperiencesFilter(filters.FilterSet):
    kw = filters.CharFilter(method='filter_kw')
    
    class Meta:
        model = Experiences
        fields = ['kw']
        
    def filter_kw(self, queryset, name, value):
        return queryset.filter(company_name__icontains=value) | \
            queryset.filter(job_title__icontains=value) | \
            queryset.filter(description__icontains=value)

class ProjectsFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Projects
        fields = ['search']
        
    def filter_search(self, queryset, name, value):
        return queryset.filter(name__icontains=value) | \
            queryset.filter(description__icontains=value)
    