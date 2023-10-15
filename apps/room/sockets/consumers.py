from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json
from json.decoder import JSONDecodeError
import os

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404

from apps.room.models import RoomUser, Room, RoomUserVote, RoomQuestion
import uuid

#Local
from ..serializers import RoomSerializer, QuestionRoomSerializer, RoomUserVoteSerializer

def uuid_to_str(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

@database_sync_to_async
def save_question(question):
    try:
        question = RoomQuestion.objects.create(
            room_id=question['room'],
            question=question['question'],
        )
        return QuestionRoomSerializer(question).data
    except Exception as e:
        print(e)
        return None

@database_sync_to_async
def delete_question(question):
    try:
        question.delete()
        return True
    except ObjectDoesNotExist:
        return False

@database_sync_to_async
def update_question(question, new_question):
    try:
        question.question = new_question['question']
        question.save()
        return QuestionRoomSerializer(question).data
    except ObjectDoesNotExist:
        return None


@database_sync_to_async
def find_question_index_by_id(question_id):
    try:
        question = RoomQuestion.objects.get(id=question_id)
        return question
    except ObjectDoesNotExist:
        return None

@database_sync_to_async
def find_question_by_id(question_id):
    try:
        question = RoomQuestion.objects.get(id=question_id)
        return question
    except ObjectDoesNotExist:
        return None

# Verificar si el usuario esta registrado en la sala y si no lo esta, agregarlo
@database_sync_to_async
def validate_user_in_room(room, user):
    try:
        room_user = RoomUser.objects.get(room=room, user=user)
    except ObjectDoesNotExist:
        room_user = RoomUser.objects.create(room=room, user=user)
    return room_user

@database_sync_to_async
def get_room_data(room):
    return RoomSerializer(room).data

@sync_to_async
def get_creator(room, user):
    return room.creator == user

@database_sync_to_async
def create_or_update_vote(user, question, vote):
    user_room = RoomUser.objects.get(user=user, room=question.room)
    try:
        room_user_vote = RoomUserVote.objects.get(
            room_user=user_room,
            question=question)
        if room_user_vote.value == vote:
            room_user_vote.delete()
            return None, None
        room_user_vote.value = vote
        room_user_vote.save()
        return (
            RoomUserVoteSerializer(room_user_vote).data
            , True)
    except ObjectDoesNotExist:
        room_user_vote = RoomUserVote.objects.create(
            room_user=user_room,
            question=question,
            value=vote)
    return (
        RoomUserVoteSerializer(room_user_vote).data
        , False)
class RoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_key = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.owner = False
        self.enable_voting = False

    @database_sync_to_async
    def get_room_or_error(self, room_key):
        try:
            room = Room.objects.get(key=room_key)
            return room
        except Room.DoesNotExist:
            raise Http404()



    async def connect(self):
        self.room_key = self.scope['url_route']['kwargs']['room_key']
        self.room_group_name = 'room_%s' % self.room_key
        self.user = self.scope['user']

        # Check if room exists
        try:
            room = await self.get_room_or_error(self.room_key)
        except Http404:
            return
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        if self.user.is_authenticated:
            room_user = await validate_user_in_room(room, self.user)
            self.enable_voting = room_user.status
            self.owner = await get_creator(room, self.user)
        data = await get_room_data(room)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notify_sale',
                'message': f'{self.user.username} has joined the room.'
            }
        )
        await self.send_room_data(
            {
                **data,
                'enable_voting': self.enable_voting,
                'owner': self.owner
            }
        )


    async def send_room_data(self, room):
        data = await sync_to_async(json.dumps)({
            'type': 'room_data',
            'room': room,
        }, cls=DjangoJSONEncoder, default=uuid_to_str)
        await self.send(text_data=data)

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            message_type = message['type']
            if message_type == 'create_question':
                question = message['question']
                room = message['room']
                question_data = {
                    'question': question,
                    'room': room
                }
                question_instance = await save_question(question_data)

                await self.create_question(question_instance)
            elif message_type == 'update_question':
                await self.update_question(message)
            elif message_type == 'delete_question':
                await self.delete_question(message)
            elif message_type == 'vote':
                await self.create_or_update_vote(message)
            elif message_type == 'chat_message':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message['message']
                    }
                )

            else:
                await self.send(text_data=json.dumps({
                    'error': 'Invalid message type'
                }))
        except JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON message.'}))
            return
        except ValueError as e:
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))

    async def create_or_update_vote(self, message):
        try:
            question_id = message['question_id']
            vote = message['vote']
            question = await find_question_by_id(question_id)
            if not self.enable_voting:
                await self.send(text_data=json.dumps({
                    'error': 'You are not allowed to vote'
                }))
            if question:
                room_user_vote, created = await create_or_update_vote(
                    self.user,
                    question,
                    vote
                )
                data = await sync_to_async(json.dumps)({
                    'type': 'vote_updated',
                    'room_user_vote': room_user_vote,
                    'update': created
                }, cls=DjangoJSONEncoder, default=uuid_to_str)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'notify_vote_updated',
                        'vote_data': data
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Question not found'
                }))
        except KeyError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))

    async def chat_message(self, event):
        message = event['message']

        # Enviar el mensaje al cliente que está conectado al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    async def update_question(self, message):
        try:
            question = await find_question_by_id(message['question_id'])
            if question:
                question_data = await update_question(question, message)
                data = await sync_to_async(json.dumps)({
                    'type': 'question_updated',
                    'question_data': question_data,
                }, cls=DjangoJSONEncoder, default=uuid_to_str)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'notify_question_updated',
                        'question_data': data
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Question not found'
                }))
        except KeyError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))

    async def delete_question(self, message):
        try:
            question = await find_question_by_id(message['question_id'])
            if question:
                delete = await delete_question(question)
                if delete:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'notify_question_deleted',
                            'question_id': message['question_id']
                        }
                    )
                else:
                    await self.send(text_data=json.dumps({
                        'error': 'Question not found, or already deleted'
                    }))
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Question not found, request failed'
                }))
        except KeyError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))

    async def notify_question_updated(self, event):
        question_data = event['question_data']
        await self.send(text_data=question_data)

    async def notify_question_deleted(self, event):
        await self.send(text_data=json.dumps({
            'type': 'question_deleted',
            'question_id': event['question_id']
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notify_sale',
                'message': f'{self.user.username} disconet.'
            }
        )
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.send(text_data=json.dumps({
            'message': f'{self.user.username} has left the room.'
        }))

    # Crear pregunta en la sala
    async def create_question(self, event):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notify_question_created',
                'question_data': event
            }
        )
    async def notify_vote_updated(self, event):
        await self.send(text_data=event['vote_data'])
    async def notify_question_created(self, event):
        question_data = event['question_data']
        await self.send(text_data=json.dumps({
            'type': 'question_created',
            'question_data': question_data
        }))

    async def notify_sale(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notify_sale',
            'message': event['message']
        }))


