from rest_framework import routers
from django.urls import path, re_path, include

# Views
from apps.user.views import UserViewSet, PermissionViewSet, GroupViewSet, LogEntryViewSet

# Routers
router = routers.DefaultRouter()
router.register(r'auth/users', UserViewSet)
router.register(r'auth/groups', GroupViewSet)
router.register(r'auth/permissions', PermissionViewSet)
router.register(r'log', LogEntryViewSet)

