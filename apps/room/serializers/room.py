# rest_framework
from rest_framework import serializers

# models
from apps.user.serializers import UserSerializer
from apps.room.models import Room, RoomQuestion, RoomUserVote
# Create your serializers here.


class QuestionRoomSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        approve = RoomUserVote.objects.filter(question=obj, value=True).count()
        disapprove = RoomUserVote.objects.filter(question=obj, value=False).count()
        return {
            'approve': approve,
            'disapprove': disapprove
        }

    class Meta:
        model = RoomQuestion
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='creator.username')
    room_question = QuestionRoomSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = '__all__'

    class RoomSerializer(serializers.ModelSerializer):
        user_name = serializers.ReadOnlyField(source='creator.username')

        class Meta:
            model = Room
            fields = '__all__'
