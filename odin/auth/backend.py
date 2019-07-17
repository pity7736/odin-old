import datetime
import typing
from starlette.authentication import AuthenticationBackend, AuthCredentials, AuthenticationError
from starlette.requests import Request

import ujson

from odin.auth.models import Token, User
from odin.utils.crypto import AES256


class OdinAuthBackend(AuthenticationBackend):

    async def authenticate(self, request: Request) -> typing.Optional[typing.Tuple['AuthCredentials', 'User']]:
        token_value = request.headers.get('Authorization')
        if token_value is None:
            return

        name, value = token_value.split(' ')
        token = await Token.get(value=value)
        if token is None:
            raise AuthenticationError('invalid token')

        aes = AES256(key=token.key, iv=token.iv)
        data = ujson.loads(aes.decrypt(value))
        token_created = datetime.datetime.fromisoformat(data['created_at'])
        if token_created < datetime.datetime.now() - datetime.timedelta(minutes=30):
            raise AuthenticationError('token expired')

        user = await User.get(id=data['user_id'])
        return AuthCredentials([]), user
