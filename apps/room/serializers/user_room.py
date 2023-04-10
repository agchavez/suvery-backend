# rest_framework
from rest_framework import serializers

# models
from apps.room.models import RoomUser, RoomUserVote

# exceptions
from apps.room.exceptions.room_user import  JoinOwnRoomError

# Create your serializers here.

class RoomUserVoteSerializer(serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(source='room_user.user.get_full_name')
    class Meta:
        model = RoomUserVote
        fields = '__all__'

    # Validar si el usuario ya voto en la pregunta
    def validate(self, data):
        if RoomUserVote.objects.filter(room_user=data['room_user'], question=data['question']).exists():
            raise serializers.ValidationError({
                'message': 'Ya has votado en esta pregunta',
                'code': 'already_voted'
            })
        return data

class RoomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomUser
        fields = '__all__'

    def validate(self, data):
        if data['user'] == data['room'].creator:
            raise JoinOwnRoomError()
        return data
