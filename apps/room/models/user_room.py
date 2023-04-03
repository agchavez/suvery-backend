from django.db import models
import uuid

# local
from apps.room.models.room import Room
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
        return self.room.key + '-' + self.user.name

    def deactivate(self):
        self.status = False
        self.save()

    def activate(self):
        self.status = True
        self.save()


