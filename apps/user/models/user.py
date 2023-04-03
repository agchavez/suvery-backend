# Django
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ['id']
        db_table = 'auth_user'


class UUIDGroup(Group):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ['id']
        db_table = 'auth_group'


class UUIDPermission(Permission):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ['id']
        db_table = 'auth_permission'


# Model User
class UserModel(models.Model):
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-created_at']
        db_table = "app_user"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    status = models.BooleanField(
        "Estado del usuario",
        default=True,
        help_text="Solo los usuarios activos pueden iniciar sesión"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
