# rest_framework
from rest_framework import serializers

# models
from apps.user.serializers import UserSerializer
from apps.room.models import Room, RoomUser


# Create your serializers here.
class RoomSerializer(serializers.ModelSerializer):
    count_users = serializers.SerializerMethodField()

    def get_count_users(self, obj):
        return RoomUser.objects.filter(room=obj).count()

    class Meta:
        model = Room
        fields = '__all__'
