# Django
from django.db import models
import uuid

from rest_framework.exceptions import ValidationError

# creation
from apps.user.models.user import UserModel


# Model by Room
class Room(models.Model):
    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['created_at']
        db_table = 'app_room'

    # id de la sala
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # key de la sala
    key = models.CharField(
        max_length=6,
        unique=True,
        blank=True,
        error_messages={
            'unique': 'Ya existe una sala con esta key',
        },
    )

    # nombre de la sala
    name = models.CharField(
        max_length=50,
    )

    # status de la sala
    status = models.BooleanField(
        default=True,
    )

    # fecha de creacion de la sala
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Creador de la sala
    creator = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='creator_room',
    )

    def __str__(self):
        return self.key

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        self.name = self.name.upper()
        super(Room, self).save(*args, **kwargs)

    def clean(self):
        if Room.objects.filter(key=self.key).exclude(id=self.id).exists():
            raise ValidationError({'key': 'Error sala con esta key ya existe'}, code='4002')

    def generate_key(self):
        import random
        import string
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    def deactivate(self):
        self.status = False
        self.save()

    def activate(self):
        self.status = True
        self.save()


# Model by Question in Room
class RoomQuestion(models.Model):
    class Meta:
        verbose_name = 'Room Question'
        verbose_name_plural = 'Room Questions'
        ordering = ['created_at']
        db_table = 'app_room_question'

    # id de la pregunta
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # pregunta
    question = models.TextField()

    # fecha de creacion de la pregunta
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # sala
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='room_question',
    )

    def __str__(self):
        return self.question
