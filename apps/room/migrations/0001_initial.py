# Generated by Django 4.1.7 on 2023-04-07 01:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(blank=True, error_messages={'unique': 'Ya existe una sala con esta key'}, max_length=6, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
                'db_table': 'app_room',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='RoomUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_user', to='room.room')),
            ],
            options={
                'verbose_name': 'RoomUser',
                'verbose_name_plural': 'RoomUsers',
                'db_table': 'app_room_user',
                'ordering': ['created_at'],
            },
        ),
    ]
