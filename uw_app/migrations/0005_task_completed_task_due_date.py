# Generated by Django 4.2.7 on 2023-11-09 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0004_category_subcategory_customuser_total_xp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
