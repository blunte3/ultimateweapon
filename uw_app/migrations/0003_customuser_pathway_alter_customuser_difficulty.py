# Generated by Django 4.2.7 on 2023-11-09 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0002_customuser_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='pathway',
            field=models.CharField(choices=[('SCHOLAR', 'SCHOLAR'), ('ATHLETE', 'ATHLETE'), ('CREATIVE', 'CREATIVE'), ('ULTIMATE WEAPON', 'ULTIMATE WEAPON')], default='ULTIMATE WEAPON', max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='difficulty',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('ULTIMATE WEAPON', 'ULTIMATE WEAPON')], default='easy', max_length=20),
        ),
    ]
