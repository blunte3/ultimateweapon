from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import JSONField


class Category(models.Model):
    name = models.CharField(max_length=255)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

class Task(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, default="daily")
    xp = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)  # Indicates whether the task is completed
    due_date = models.DateTimeField(null=True, blank=True)  # Due date for the task


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    character_image = models.CharField(max_length=255, default="../images/jainar.jpg")
    display_name = models.CharField(max_length=255, default="Default Name")
    pathway = models.ManyToManyField(Subcategory, related_name='pathway', blank=True)
    difficulty = models.CharField(max_length=20, choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard"), ("ULTIMATE WEAPON", "ULTIMATE WEAPON")], default="Easy")    
    total_xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    daily_tasks = models.ManyToManyField(Task, related_name='daily_tasks', blank=True)
    weekly_tasks = models.ManyToManyField(Task, related_name='weekly_tasks', blank=True)
    monthly_tasks = models.ManyToManyField(Task, related_name='monthly_tasks', blank=True)

    last_daily_tasks_refreshed = models.DateTimeField(default=timezone.now)
    last_weekly_tasks_refreshed = models.DateTimeField(default=timezone.now)
    last_monthly_tasks_refreshed = models.DateTimeField(default=timezone.now)