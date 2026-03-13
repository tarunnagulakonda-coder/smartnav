from django.urls import path
from . import views

urlpatterns = [
    path('editor/', views.admin_editor_view, name='indoor_editor'),
    path('api/add-building/', views.api_add_building, name='api_add_building'),
    path('editor/floor/<int:floor_id>/', views.floor_editor_view, name='floor_editor'),
    path('api/save-rooms/', views.api_save_rooms, name='api_save_rooms'),
    path('api/save-nav-steps/', views.api_save_nav_steps, name='api_save_nav_steps'),
    path('building/<int:building_id>/3d/', views.building_3d_view, name='building_3d'),
    path('api/building/<int:building_id>/', views.api_building_data, name='api_building_data'),
]
