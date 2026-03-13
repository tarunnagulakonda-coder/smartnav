from django.db import models

class Block(models.Model):
    block_name = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.block_name

class Faculty(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    cabin_block = models.ForeignKey(Block, on_delete=models.CASCADE)
    cabin_room = models.CharField(max_length=50)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    availability = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.name

class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic_name

class Student(models.Model):
    registration_no = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.registration_no

class FacultyUser(models.Model):
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE)
    login_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.login_id

class TimetableSettings(models.Model):
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE)
    working_days = models.IntegerField(default=6)
    periods_per_day = models.IntegerField(default=8)

    def __str__(self):
        return f"{self.faculty.name} Settings"

class PeriodTime(models.Model):
    settings = models.ForeignKey(TimetableSettings, on_delete=models.CASCADE)
    period_number = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Period {self.period_number} ({self.start_time}-{self.end_time})"

class WeeklySchedule(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('In Class', 'In Class'),
    )
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    period_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.faculty.name} - {self.day} - P{self.period_number} - {self.status}"
