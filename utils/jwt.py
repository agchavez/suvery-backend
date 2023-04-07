from datetime import datetime, timedelta
import jwt
from django.conf import settings


class JWTManager:
    @staticmethod
    def generate_token(user_email, user_id, expiration_time_hours):
        """
        Generates a JWT token for the given user email and user ID, with a variable expiration time.
        """
        exp_time = datetime.utcnow() + timedelta(hours=expiration_time_hours)
        payload = {
            'email': user_email,
            'id': user_id,
            'exp': exp_time,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def decode_token(token):
        """
        Decodes and returns the payload of the given JWT token, if it is valid.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            # The token has expired
            return None
        except jwt.InvalidTokenError:
            # The token is invalid
            return None
