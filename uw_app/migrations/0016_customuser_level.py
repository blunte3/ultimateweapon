# Generated by Django 4.2.7 on 2023-11-22 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0015_category_level_subcategory_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
