# rest_framework

from rest_framework import mixins, viewsets

# models
from apps.room.models import Room, RoomQuestion

# serializers
from apps.room.serializers.room import RoomSerializer, QuestionRoomSerializer

# log
from django.contrib.admin.models import LogEntry

# Create your views here.
class RoomViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


    def perform_create(self, serializer):
        serializer =  serializer.save()
        print('perform_create', serializer)

        return serializer

class QuestionRoomViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = RoomQuestion.objects.all()
    serializer_class = QuestionRoomSerializer

