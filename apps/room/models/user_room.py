from django.db import models
import uuid

# local
from apps.room.models.room import Room, RoomQuestion
from apps.user.models.user import UserModel


# Create your models here.
class RoomUser(models.Model):
    class Meta:
        verbose_name = 'RoomUser'
        verbose_name_plural = 'RoomUsers'
        ordering = ['created_at']
        db_table = 'app_room_user'

    # id de la sala
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # status de la sala
    status = models.BooleanField(
        default=True,
    )

    # fecha de creacion de la sala
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Relacion de la sala
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='room_user',
    )

    # Relacion del usuario
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='user_room',
    )

    def __str__(self):
        return self.room.key + '-' + self.user.username

    def deactivate(self):
        self.status = False
        self.save()

    def activate(self):
        self.status = True
        self.save()



# Create Model by User vote in question room
class RoomUserVote(models.Model):
    class Meta:
        verbose_name = 'RoomUserVote'
        verbose_name_plural = 'RoomUserVotes'
        ordering = ['created_at']
        db_table = 'app_room_user_vote'

    # id de la sala
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # status de la sala
    value = models.BooleanField()

    # fecha de creacion de la sala
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Relacion de la sala
    room_user = models.ForeignKey(
        RoomUser,
        on_delete=models.CASCADE,
        related_name='room_user_vote',
    )
    # Relacion de la pregunta
    question = models.ForeignKey(
        RoomQuestion,
        on_delete=models.CASCADE,
        related_name='question_user_vote',
    )

    def __str__(self):
        return self.id

