from django_filters import rest_framework as filters
from info.models import Blogs, Experiences, Projects


class BlogsFilter(filters.FilterSet):
    """Filter for blog search by keyword and skills"""
    kw = filters.CharFilter(method='filter_kw')
    skills = filters.CharFilter(method='filter_skills')
    skill_ids = filters.CharFilter(method='filter_skill_ids')

    class Meta:
        model = Blogs
        fields = ['kw', 'skills', 'skill_ids']

    def filter_kw(self, queryset, name, value):
        return queryset.filter(title__icontains=value) | \
            queryset.filter(content__icontains=value) | \
            queryset.filter(description__icontains=value)

    def filter_skills(self, queryset, name, value):
        if not value:
            return queryset

        skill_names = [skill.strip() for skill in value.split(',')]
        for skill_name in skill_names:
            queryset = queryset.filter(skills__name=skill_name)
        return queryset.distinct()

    def filter_skill_ids(self, queryset, name, value):
        if not value:
            return queryset

        try:
            skill_ids = [int(skill_id.strip()) for skill_id in value.split(',')]
            for skill_id in skill_ids:
                queryset = queryset.filter(skills__id=skill_id)
            return queryset.distinct()
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
    