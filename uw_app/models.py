from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import JSONField


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    character_image = models.CharField(max_length=255, default="images/jainar.jpg")
    display_name = models.CharField(max_length=255, default="Default Name")
    difficulty = models.CharField(max_length=20, choices=[("Easy","Easy"), ("Medium","Medium"), ("Hard","Hard"), ("ULTIMATE WEAPON","ULTIMATE WEAPON")], default="Easy")
    pathway = models.CharField(max_length=20, choices=[("SCHOLAR","SCHOLAR"),("ATHLETE","ATHLETE"),("CREATIVE","CREATIVE"),("ULTIMATE WEAPON","ULTIMATE WEAPON")], default="ULTIMATE WEAPON")
    total_xp = models.IntegerField(default=0)

    short_tasks = models.JSONField(default=list)
    medium_tasks = models.JSONField(default=list)
    long_tasks = models.JSONField(default=list)

    last_short_tasks_refreshed = models.DateTimeField(default=timezone.now)
    last_medium_tasks_refreshed = models.DateTimeField(default=timezone.now)
    last_long_tasks_refreshed = models.DateTimeField(default=timezone.now)

class Category(models.Model):
    name = models.CharField(max_length=255)
    xp = models.IntegerField(default=0)

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)

class Task(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)  # Indicates whether the task is completed
    due_date = models.DateTimeField(null=True, blank=True)  # Due date for the task
