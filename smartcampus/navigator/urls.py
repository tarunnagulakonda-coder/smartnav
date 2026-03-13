from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('map/', views.map_view, name='map'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('faculty-search/', views.faculty_search_view, name='faculty_search'),
    path('block-search/', views.block_search_view, name='block_search'),
    path('api/locations/', views.get_locations, name='get_locations'),
    path('api/faculty/', views.api_faculty_search, name='api_faculty_search'),
    path('api/blocks/', views.api_block_search, name='api_block_search'),
    # Faculty timetable system
    path('faculty-login/', views.faculty_login_view, name='faculty_login'),
    path('faculty-dashboard/', views.faculty_dashboard_view, name='faculty_dashboard'),
    path('timetable/config/', views.timetable_config_view, name='timetable_config'),
    path('timetable/periods/', views.period_times_view, name='period_times'),
    path('timetable/schedule/', views.weekly_schedule_view, name='weekly_schedule'),
]
