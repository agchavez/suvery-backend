from rest_framework import routers
from django.urls import path, include

# Views
from apps.auth.views import AuthView

# Routers
router = routers.DefaultRouter()
router.register(r'auth', AuthView, basename='auth')
