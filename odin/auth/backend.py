import datetime
import typing
from starlette.authentication import AuthenticationBackend, AuthCredentials, AuthenticationError
from starlette.requests import Request

import ujson

from odin.auth.models import Token, User
from odin.settings import TOKEN_EXPIRATION_MINUTES_DELTA
from odin.utils.crypto import AES256


class OdinAuthBackend(AuthenticationBackend):

    async def authenticate(self, request: Request) -> typing.Optional[typing.Tuple['AuthCredentials', 'User']]:
        token_value = request.headers.get('Authorization')
        if token_value is None:
            return

        try:
            name, value = token_value.split(' ')
        except ValueError:
            raise AuthenticationError('invalid token')

        token = await Token.get(value=value)
        if token is None or name != 'Bearer':
            raise AuthenticationError('invalid token')

        aes = AES256(key=token.key, iv=token.iv)
        data = ujson.loads(aes.decrypt(value))
        token_created = datetime.datetime.fromisoformat(data['created_at'])
        if token_created < datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES_DELTA):
            raise AuthenticationError('token expired')

        user = await User.get(id=data['user_id'])
        return AuthCredentials([]), user
