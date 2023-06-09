# Generated by Django 4.1.7 on 2023-04-07 05:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_question', to='room.room')),
            ],
            options={
                'verbose_name': 'Room Question',
                'verbose_name_plural': 'Room Questions',
                'db_table': 'app_room_question',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='RoomUserVote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_user_vote', to='room.roomquestion')),
                ('room_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_user_vote', to='room.roomuser')),
            ],
            options={
                'verbose_name': 'RoomUserVote',
                'verbose_name_plural': 'RoomUserVotes',
                'db_table': 'app_room_user_vote',
                'ordering': ['created_at'],
            },
        ),
    ]
