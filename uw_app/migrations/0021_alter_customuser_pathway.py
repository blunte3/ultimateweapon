# Generated by Django 4.2.7 on 2023-12-01 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0020_alter_subsubcategory_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pathway',
            field=models.ManyToManyField(blank=True, related_name='pathway', to='uw_app.subsubcategory'),
        ),
    ]
