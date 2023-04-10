# rest_framework

from rest_framework import mixins, viewsets

# models
from apps.room.models import RoomUser, RoomUserVote

# serializers
from apps.room.serializers import RoomUserSerializer,RoomUserVoteSerializer


# Create your views here.
class RoomUserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = RoomUser.objects.all()
    serializer_class = RoomUserSerializer


class RoomUserVoteViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
        queryset = RoomUserVote.objects.all()
        serializer_class = RoomUserVoteSerializer
