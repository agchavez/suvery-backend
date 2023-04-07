from django.contrib import admin
from .models import RoomUser, Room,RoomQuestion, RoomUserVote

# Register your models here.
admin.site.register(RoomUser)
admin.site.register(Room)
admin.site.register(RoomQuestion)
admin.site.register(RoomUserVote)