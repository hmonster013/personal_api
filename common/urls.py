from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('all-configs', views.get_all_config, name='all-configs'),

    path('skills/list', views.SkillsListView.as_view(), name='skills-list'),
    path('links/list', views.LinksListView.as_view(), name='links-list'),
    path('links/view/<str:name>', views.LinksDetailView.as_view(), name='links-detail'),

    path('contacts/create', views.ContactCreateView.as_view(), name='contact-create'),
]