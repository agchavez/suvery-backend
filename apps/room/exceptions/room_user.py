from rest_framework import status
from rest_framework.exceptions import APIException


class JoinOwnRoomError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'No puedes unirte a tu propia sala'
    default_code = '4011'

# Ya existe registro
class RoomUserAlreadyExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ya existe registro'
    default_code = '4010'
