import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import CampusBuilding, BuildingFloor, Room, NavigationStep


def admin_editor_view(request):
    """Campus map editor - admin clicks to add buildings."""
    buildings = CampusBuilding.objects.all()
    buildings_data = []
    for b in buildings:
        buildings_data.append({
            'id': b.id,
            'name': b.name,
            'lat': b.latitude,
            'lng': b.longitude,
            'num_floors': b.num_floors,
        })
    return render(request, "indoor/indoor_editor.html", {
        'buildings': buildings,
        'buildings_json': json.dumps(buildings_data),
    })


@csrf_exempt
def api_add_building(request):
    """POST: Create building + auto-create floors."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data = json.loads(request.body)
    name = data.get('name', '').strip()
    lat = data.get('lat')
    lng = data.get('lng')
    num_floors = int(data.get('num_floors', 1))

    if not name:
        return JsonResponse({'error': 'Name required'}, status=400)

    building = CampusBuilding.objects.create(
        name=name, latitude=lat, longitude=lng, num_floors=num_floors
    )

    # Auto-create floor records
    for i in range(1, num_floors + 1):
        BuildingFloor.objects.create(building=building, floor_number=i)

    return JsonResponse({
        'id': building.id,
        'name': building.name,
        'num_floors': building.num_floors,
    })


def floor_editor_view(request, floor_id):
    """Grid editor for placing room nodes on a floor."""
    floor = get_object_or_404(BuildingFloor, pk=floor_id)
    building = floor.building
    all_floors = building.floors.all()
    rooms = Room.objects.filter(floor=floor)
    rooms_data = [{'id': r.id, 'name': r.room_name, 'x': r.x_pos, 'y': r.y_pos} for r in rooms]

    return render(request, "indoor/floor_editor.html", {
        'floor': floor,
        'building': building,
        'all_floors': all_floors,
        'rooms_json': json.dumps(rooms_data),
    })


@csrf_exempt
def api_save_rooms(request):
    """POST: Save room nodes for a floor."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data = json.loads(request.body)
    floor_id = data.get('floor_id')
    rooms = data.get('rooms', [])

    floor = get_object_or_404(BuildingFloor, pk=floor_id)
    Room.objects.filter(floor=floor).delete()

    for r in rooms:
        Room.objects.create(
            floor=floor,
            room_name=r['name'],
            x_pos=r['x'],
            y_pos=r['y']
        )

    return JsonResponse({'status': 'ok', 'count': len(rooms)})


@csrf_exempt
def api_save_nav_steps(request):
    """POST: Save navigation steps for a room."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data = json.loads(request.body)
    room_id = data.get('room_id')
    steps = data.get('steps', [])

    room = get_object_or_404(Room, pk=room_id)
    NavigationStep.objects.filter(room=room).delete()

    for i, text in enumerate(steps, 1):
        NavigationStep.objects.create(room=room, step_order=i, instruction=text)

    return JsonResponse({'status': 'ok', 'count': len(steps)})


def building_3d_view(request, building_id):
    """3D building view with Three.js + voice nav."""
    building = get_object_or_404(CampusBuilding, pk=building_id)
    return render(request, "indoor/building_3d.html", {
        'building': building,
        'building_id': building.id,
    })


def api_building_data(request, building_id):
    """GET: Full building data for 3D rendering."""
    building = get_object_or_404(CampusBuilding, pk=building_id)
    floors_data = []
    for floor in building.floors.all():
        rooms_data = []
        for room in floor.rooms.all():
            steps = list(room.nav_steps.values('step_order', 'instruction'))
            rooms_data.append({
                'id': room.id,
                'name': room.room_name,
                'x': room.x_pos,
                'y': room.y_pos,
                'nav_steps': steps,
            })
        floors_data.append({
            'floor_number': floor.floor_number,
            'rooms': rooms_data,
        })

    return JsonResponse({
        'id': building.id,
        'name': building.name,
        'num_floors': building.num_floors,
        'floors': floors_data,
    })
