# Django
from django.db import models
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
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

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Obtén el objeto ChannelLayer

@receiver(post_save, sender=Room)
def mi_modelo_post_save(sender, instance, **kwargs):
    # Código que se ejecutará después de guardar un objeto MiModelo
    print('post_save', instance)
    # Llamada a la función para enviar un mensaje a la sala
    group_name = "room_%s" % instance.key
    message = 'Mensaje que deseas enviar a la sala'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "message": "Este es mi mensaje de chat"
        }
    )
    # Define la función para enviar un mensaje a la sala
