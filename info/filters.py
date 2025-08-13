from django_filters import rest_framework as filters
from info.models import Blogs, Experiences, Projects


class BlogsFilter(filters.FilterSet):
    kw = filters.CharFilter(method='filter_kw')
    skills = filters.CharFilter(method='filter_skills')
    skill_ids = filters.CharFilter(method='filter_skill_ids')

    class Meta:
        model = Blogs
        fields = ['kw', 'skills', 'skill_ids']

    def filter_kw(self, queryset, name, value):
        """Tìm kiếm theo keyword trong title, content, description"""
        return queryset.filter(title__icontains=value) | \
            queryset.filter(content__icontains=value) | \
            queryset.filter(description__icontains=value)

    def filter_skills(self, queryset, name, value):
        """Tìm kiếm theo tên skill (có thể truyền nhiều skill cách nhau bởi dấu phẩy)"""
        if not value:
            return queryset

        skill_names = [skill.strip() for skill in value.split(',')]
        return queryset.filter(skills__name__in=skill_names).distinct()

    def filter_skill_ids(self, queryset, name, value):
        """Tìm kiếm theo ID của skill (có thể truyền nhiều ID cách nhau bởi dấu phẩy)"""
        if not value:
            return queryset

        try:
            skill_ids = [int(skill_id.strip()) for skill_id in value.split(',')]
            return queryset.filter(skills__id__in=skill_ids).distinct()
        except ValueError:
            return queryset.none()

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
    