# Generated by Django 4.2.7 on 2023-11-21 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0013_alter_customuser_character_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='pathway',
        ),
        migrations.AddField(
            model_name='customuser',
            name='pathway',
            field=models.ManyToManyField(blank=True, related_name='pathway', to='uw_app.subcategory'),
        ),
    ]
