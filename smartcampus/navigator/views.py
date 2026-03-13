from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Block, Faculty, Topic, Student, FacultyUser, TimetableSettings, PeriodTime, WeeklySchedule
from datetime import datetime

def get_locations(request):
    blocks = Block.objects.all()
    data = []
    for b in blocks:
        data.append({
            "name": b.block_name,
            "lat": b.latitude,
            "lng": b.longitude,
            "type": b.department or "General"
        })
    return JsonResponse(data, safe=False)

def search_topic(request):
    q = request.GET.get("q", "")
    topics = Topic.objects.filter(topic_name__icontains=q)
    result = []
    for t in topics:
        result.append({
            "faculty": t.faculty.name,
            "location": f"{t.faculty.cabin_block.block_name} - {t.faculty.cabin_room}",
            "room": t.faculty.cabin_room,
            "specialization": t.faculty.specialization,
            "lat": t.faculty.latitude,
            "lng": t.faculty.longitude,
            "availability": t.faculty.availability
        })
    return JsonResponse(result, safe=False)

def map_view(request):
    role = request.session.get('role', 'visitor') 
    if 'role' not in request.session:
        return redirect('login')
    
    dest_lat = request.GET.get('dest_lat')
    dest_lng = request.GET.get('dest_lng')
    dest_name = request.GET.get('dest_name')
    
    building_id = request.GET.get('building_id')
    return render(request, "map.html", {
        "role": role, 
        "dest_lat": dest_lat, 
        "dest_lng": dest_lng, 
        "dest_name": dest_name,
        "building_id": building_id
    })

def dashboard_view(request):
    if request.session.get('role') != 'student':
        return redirect('map')
    return render(request, "dashboard.html")

def faculty_search_view(request):
    if request.session.get('role') != 'student':
        return redirect('map')
    return render(request, "faculty_search.html")

def block_search_view(request):
    if 'role' not in request.session:
        return redirect('login')
    return render(request, "block_search.html")


# ========================================
# Helper: Get real-time faculty availability
# ========================================
def get_realtime_availability(faculty):
    """Check timetable to determine if faculty is currently available."""
    now = datetime.now()
    current_day = now.strftime('%A')
    current_time = now.time()

    try:
        settings = TimetableSettings.objects.get(faculty=faculty)
    except TimetableSettings.DoesNotExist:
        return faculty.availability  # No timetable configured, use static field

    # Find current period
    period = PeriodTime.objects.filter(
        settings=settings,
        start_time__lte=current_time,
        end_time__gte=current_time
    ).first()

    if not period:
        return "Available"  # Outside class hours

    # Check weekly schedule
    schedule = WeeklySchedule.objects.filter(
        faculty=faculty,
        day=current_day,
        period_number=period.period_number
    ).first()

    if schedule:
        return schedule.status
    return "Available"


def api_faculty_search(request):
    q = request.GET.get('q', '').lower()
    faculties = Faculty.objects.all()
    
    data = []
    for f in faculties:
        if q and q not in f.name.lower() and q not in f.department.lower() and q not in f.specialization.lower():
            continue
        
        # Use real-time availability from timetable
        availability = get_realtime_availability(f)
        
        data.append({
            "name": f.name,
            "department": f.department,
            "specialization": f.specialization,
            "location": f"{f.cabin_block.block_name} - {f.cabin_room}",
            "lat": f.latitude,
            "lng": f.longitude,
            "availability": availability
        })
    return JsonResponse(data, safe=False)

def api_block_search(request):
    from indoor.models import CampusBuilding
    q = request.GET.get('q', '').lower()
    buildings = CampusBuilding.objects.all()
    
    data = []
    for b in buildings:
        if q and q not in b.name.lower():
            continue
        data.append({
            "id": b.id,
            "name": b.name,
            "department": "Campus Building",
            "num_floors": b.num_floors,
            "lat": b.latitude,
            "lng": b.longitude
        })
    return JsonResponse(data, safe=False)

def login_view(request):
    error = None
    if request.method == "POST":
        login_type = request.POST.get("login_type")
        if login_type == "student":
            reg_no = request.POST.get("reg_no", "").strip()
            password = request.POST.get("password", "").strip()
            try:
                student = Student.objects.get(registration_no=reg_no)
                if student.password == password:
                    request.session['role'] = 'student'
                    request.session['reg_no'] = reg_no
                    return redirect('dashboard')
                else:
                    error = "Invalid password. Please try again."
            except Student.DoesNotExist:
                error = "Registration number not found."
        elif login_type == "visitor":
            request.session['role'] = 'visitor'
            return redirect('map')
            
    return render(request, "login.html", {"error": error})


# ========================================
# FACULTY LOGIN & TIMETABLE VIEWS
# ========================================

def faculty_login_view(request):
    error = None
    if request.method == "POST":
        login_id = request.POST.get("login_id", "").strip()
        password = request.POST.get("password", "").strip()
        try:
            fuser = FacultyUser.objects.get(login_id=login_id)
            if fuser.password == password:
                request.session['role'] = 'faculty'
                request.session['faculty_pk'] = fuser.faculty.pk
                request.session['faculty_name'] = fuser.faculty.name
                return redirect('faculty_dashboard')
            else:
                error = "Invalid password."
        except FacultyUser.DoesNotExist:
            error = "Faculty ID not found."
    return render(request, "faculty_login.html", {"error": error})


def faculty_dashboard_view(request):
    if request.session.get('role') != 'faculty':
        return redirect('login')
    
    faculty_pk = request.session.get('faculty_pk')
    faculty = Faculty.objects.get(pk=faculty_pk)
    
    has_timetable = TimetableSettings.objects.filter(faculty=faculty).exists()
    settings = None
    period_times = []
    timetable_rows = []

    if has_timetable:
        settings = TimetableSettings.objects.get(faculty=faculty)
        period_times = list(PeriodTime.objects.filter(settings=settings).order_by('period_number'))
        
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_list = all_days[:settings.working_days]
        
        # Build a lookup dict
        entries = WeeklySchedule.objects.filter(faculty=faculty)
        schedule_lookup = {}
        for entry in entries:
            schedule_lookup[f"{entry.day}_P{entry.period_number}"] = entry.status
        
        # Build rows: each row = { "day": "Monday", "cells": ["Available", "In Class", ...] }
        for day in days_list:
            cells = []
            for pt in period_times:
                key = f"{day}_P{pt.period_number}"
                cells.append(schedule_lookup.get(key, "—"))
            timetable_rows.append({"day": day, "cells": cells})

    return render(request, "faculty_dashboard.html", {
        "faculty": faculty,
        "has_timetable": has_timetable,
        "settings": settings,
        "period_times": period_times,
        "timetable_rows": timetable_rows,
    })


def timetable_config_view(request):
    if request.session.get('role') != 'faculty':
        return redirect('login')
    
    faculty_pk = request.session.get('faculty_pk')
    faculty = Faculty.objects.get(pk=faculty_pk)
    
    if request.method == "POST":
        working_days = int(request.POST.get('working_days', 6))
        periods_per_day = int(request.POST.get('periods_per_day', 8))
        
        settings, created = TimetableSettings.objects.update_or_create(
            faculty=faculty,
            defaults={'working_days': working_days, 'periods_per_day': periods_per_day}
        )
        # Clear old period times if editing
        PeriodTime.objects.filter(settings=settings).delete()
        
        return redirect('period_times')
    
    return render(request, "timetable_config.html", {"faculty": faculty})


def period_times_view(request):
    if request.session.get('role') != 'faculty':
        return redirect('login')
    
    faculty_pk = request.session.get('faculty_pk')
    faculty = Faculty.objects.get(pk=faculty_pk)
    settings = TimetableSettings.objects.get(faculty=faculty)
    
    if request.method == "POST":
        PeriodTime.objects.filter(settings=settings).delete()
        
        for i in range(1, settings.periods_per_day + 1):
            start = request.POST.get(f'start_{i}')
            end = request.POST.get(f'end_{i}')
            if start and end:
                PeriodTime.objects.create(
                    settings=settings,
                    period_number=i,
                    start_time=start,
                    end_time=end
                )
        
        return redirect('weekly_schedule')
    
    periods_range = range(1, settings.periods_per_day + 1)
    return render(request, "period_times.html", {
        "faculty": faculty,
        "settings": settings,
        "periods_range": periods_range
    })


def weekly_schedule_view(request):
    if request.session.get('role') != 'faculty':
        return redirect('login')
    
    faculty_pk = request.session.get('faculty_pk')
    faculty = Faculty.objects.get(pk=faculty_pk)
    settings = TimetableSettings.objects.get(faculty=faculty)
    period_times = PeriodTime.objects.filter(settings=settings).order_by('period_number')
    
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days = all_days[:settings.working_days]
    
    if request.method == "POST":
        WeeklySchedule.objects.filter(faculty=faculty).delete()
        
        for day in days:
            for pt in period_times:
                status = request.POST.get(f'{day}_P{pt.period_number}', 'Available')
                WeeklySchedule.objects.create(
                    faculty=faculty,
                    day=day,
                    period_number=pt.period_number,
                    status=status
                )
        
        return redirect('faculty_dashboard')
    
    return render(request, "weekly_schedule.html", {
        "faculty": faculty,
        "settings": settings,
        "period_times": period_times,
        "days": days
    })
