from django.contrib import admin
from .models import Block, Faculty, Topic, Student, FacultyUser, TimetableSettings, PeriodTime, WeeklySchedule

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('block_name', 'department', 'latitude', 'longitude')
    search_fields = ('block_name', 'department')
    list_filter = ('department',)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'specialization', 'cabin_block', 'cabin_room', 'availability')
    search_fields = ('name', 'department', 'specialization')
    list_filter = ('department', 'availability', 'cabin_block')
    list_editable = ('availability',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_name', 'faculty')
    search_fields = ('topic_name', 'faculty__name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_no',)
    search_fields = ('registration_no',)

admin.site.register(FacultyUser)
admin.site.register(TimetableSettings)

@admin.register(PeriodTime)
class PeriodTimeAdmin(admin.ModelAdmin):
    list_display = ('settings', 'period_number', 'start_time', 'end_time')

@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'day', 'period_number', 'status')
    list_filter = ('day', 'status')
