# Generated by Django 4.1 on 2024-03-17 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_alter_todo_obj_created_alter_todo_obj_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo_obj',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='todo_obj',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
