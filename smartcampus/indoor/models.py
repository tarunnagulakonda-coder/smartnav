from django.db import models

class CampusBuilding(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    num_floors = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class BuildingFloor(models.Model):
    building = models.ForeignKey(CampusBuilding, on_delete=models.CASCADE, related_name='floors')
    floor_number = models.IntegerField()

    class Meta:
        ordering = ['floor_number']

    def __str__(self):
        return f"{self.building.name} - Floor {self.floor_number}"

class Room(models.Model):
    floor = models.ForeignKey(BuildingFloor, on_delete=models.CASCADE, related_name='rooms')
    room_name = models.CharField(max_length=200)
    x_pos = models.IntegerField()  # grid column
    y_pos = models.IntegerField()  # grid row

    def __str__(self):
        return f"{self.room_name} (Floor {self.floor.floor_number}, {self.floor.building.name})"

class NavigationStep(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='nav_steps')
    step_order = models.IntegerField()
    instruction = models.CharField(max_length=500)

    class Meta:
        ordering = ['step_order']

    def __str__(self):
        return f"Step {self.step_order}: {self.instruction}"
