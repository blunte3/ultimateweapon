# Generated by Django 4.2.7 on 2023-11-22 05:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0016_customuser_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='due_date',
        ),
        migrations.AddField(
            model_name='customuser',
            name='daily_due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 22, 5, 5, 58, 481591, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='customuser',
            name='monthly_due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 22, 5, 5, 58, 481591, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='customuser',
            name='weekly_due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 22, 5, 5, 58, 481591, tzinfo=datetime.timezone.utc)),
        ),
    ]