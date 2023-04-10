from rest_framework import routers
from django.urls import path, re_path, include

# Views
from apps.room.views import RoomViewSet, RoomUserViewSet, QuestionRoomViewSet, RoomUserVoteViewSet

# Routers
router = routers.DefaultRouter()
router.register(r'room', RoomViewSet)
router.register(r'question_room', QuestionRoomViewSet)
router.register(r'room_user', RoomUserViewSet)
router.register(r'room_user_vote', RoomUserVoteViewSet)

