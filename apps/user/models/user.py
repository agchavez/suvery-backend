from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
import uuid
class UserModel(AbstractUser):
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-created_at']
        db_table = "auth_user"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    first_name = models.CharField(
        'first name',
        max_length=60,
        error_messages={
            'required': 'El nombre es es obligatorio',
            'max_length': 'El nombre debe tener menos de 60 caracteres'
        }
    )
    last_name = models.CharField(
        'last name',
        max_length=60,
        error_messages={
            'required': 'El apellido es obligatorio',
            'max_length': 'El apellido debe tener menos de 60 caracteres'
        }
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'required': 'El email es obligatorio',
            'unique': 'El email ya existe'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name