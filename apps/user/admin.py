from django.contrib import admin
from apps.user.models import UserModel
from django.contrib.auth.models import Permission, ContentType

# Register your models here.
admin.site.register(UserModel)
admin.site.register(Permission)
admin.site.register(ContentType)