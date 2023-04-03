# rest_framework
from rest_framework import serializers

# models
from apps.user.serializers import UserSerializer
from apps.room.models import RoomUser

# exceptions
from apps.room.exceptions.room_user import RoomUserAlreadyExistsError, JoinOwnRoomError

# Create your serializers here.
class RoomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomUser
        fields = '__all__'

    def validate(self, data):
        if data['user'] == data['room'].creator:
            raise JoinOwnRoomError()
        return data
