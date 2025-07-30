from django.urls import path

from info.views import BlogsDetailView, BlogsListView, ExperiencesDetailView, ExperiencesListView, ProjectsDetailView, ProjectsListView

app_name = 'info'

urlpatterns = [
    path('blogs/list', BlogsListView.as_view(), name='blogs-list'),
    path('blogs/view/<int:id>', BlogsDetailView.as_view(), name='blogs-detail'),
    path('experiences/list', ExperiencesListView.as_view(), name='experiences-list'),
    path('experiences/view/<int:id>', ExperiencesDetailView.as_view(), name='experiences-detail'),
    path('projects/list', ProjectsListView.as_view(), name='projects-list'),
    path('projects/view/<int:id>', ProjectsDetailView.as_view(), name='projects-detail'),
]
