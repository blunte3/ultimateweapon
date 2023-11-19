# Generated by Django 4.2.7 on 2023-11-09 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uw_app', '0003_customuser_pathway_alter_customuser_difficulty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('xp', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('xp', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uw_app.category')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='total_xp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='difficulty',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('ULTIMATE WEAPON', 'ULTIMATE WEAPON')], default='Easy', max_length=20),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('xp', models.IntegerField(default=0)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uw_app.subcategory')),
            ],
        ),
    ]