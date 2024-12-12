# Generated by Django 5.1.4 on 2024-12-12 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_list_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='tasks',
        ),
        migrations.AddField(
            model_name='task',
            name='list_key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.list'),
        ),
    ]