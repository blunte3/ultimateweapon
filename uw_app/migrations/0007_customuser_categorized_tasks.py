# Generated by Django 4.2.7 on 2023-11-11 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0006_customuser_last_long_tasks_refreshed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='categorized_tasks',
            field=models.JSONField(default=dict),
        ),
    ]
