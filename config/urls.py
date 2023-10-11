from django.contrib import admin
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, re_path, include
from apps.user.url import router as user_router
from apps.room.url import router as room_router
from apps.auth.url import router as auth_router
router = DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(room_router.registry)
router.registry.extend(auth_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

