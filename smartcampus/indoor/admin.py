from django.contrib import admin
from .models import CampusBuilding, BuildingFloor, Room, NavigationStep

class FloorInline(admin.TabularInline):
    model = BuildingFloor
    extra = 0

class RoomInline(admin.TabularInline):
    model = Room
    extra = 0

class NavStepInline(admin.TabularInline):
    model = NavigationStep
    extra = 0

@admin.register(CampusBuilding)
class CampusBuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_floors', 'latitude', 'longitude')
    inlines = [FloorInline]

@admin.register(BuildingFloor)
class BuildingFloorAdmin(admin.ModelAdmin):
    list_display = ('building', 'floor_number')
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'floor', 'x_pos', 'y_pos')
    inlines = [NavStepInline]

@admin.register(NavigationStep)
class NavigationStepAdmin(admin.ModelAdmin):
    list_display = ('room', 'step_order', 'instruction')
