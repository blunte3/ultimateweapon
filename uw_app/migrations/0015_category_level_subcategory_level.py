# Generated by Django 4.2.7 on 2023-11-22 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0014_remove_customuser_pathway_customuser_pathway'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
