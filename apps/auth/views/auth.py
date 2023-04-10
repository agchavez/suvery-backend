

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import  Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import update_last_login
from django.views.decorators.csrf import csrf_exempt

from utils.jwt import JWTManager
#Local
from ..serializers import LoginSerializer
from apps.user.serializers import UserSerializer
from rest_framework.authtoken.models import Token

class AuthView(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user is not None:
            update_last_login(None, user)
            # el token durará 24 horas
            token = JWTManager.generate_token(user_email=user.email, user_id=user.id, expiration_time_hours=24)
            return Response({
                'user': UserSerializer(user).data,
                'token': token
            })
        else:
            return Response({
                'error': 'Credenciales inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=False)
    def logout(self, request):
        logout(request)
        return Response({'success': 'Sesión cerrada correctamente'})
