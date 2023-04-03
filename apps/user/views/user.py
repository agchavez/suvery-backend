# Rest_framework
from rest_framework import mixins, viewsets

# Models
from apps.user.models import UserModel
from django.contrib.auth.models import Group, Permission, User

# Log de administrador
from django.contrib.admin.models import LogEntry

# Serializers
from apps.user.serializers import (UserSerializer,
                                   GroupSerializer,
                                   PermissionSerializer,
                                   LogEntrySerializer)

# filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework.filters import SearchFilter, OrderingFilter


# ViewSets by UserModel
class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'email', 'first_name', 'last_name')


# ViewSets by Group
class GroupViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# ViewSets by Permission
class PermissionViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('name', 'codename')
    filter_fields = ('content_type',)


# Filter by log
class LogEntryFilter(django_filters.FilterSet):
    user = django_filters.ModelMultipleChoiceFilter(
        field_name='user__username',
        to_field_name='username',
        queryset=User.objects.all()

    )
    content_type = django_filters.CharFilter(field_name='content_type__model', lookup_expr='icontains')
    change_message = django_filters.CharFilter(field_name='change_message', lookup_expr='icontains')

    class Meta:
        model = LogEntry
        fields = ['user', 'content_type', 'action_flag', 'change_message']


# ViewSets by LogEntry
class LogEntryViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = LogEntryFilter
    search_fields = ('user__username', 'content_type__model', 'action_flag', 'change_message')
    ordering_fields = ('user__username', 'content_type__model', 'action_flag', 'change_message')