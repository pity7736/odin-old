import typing
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser
from starlette.requests import Request

# from odin.auth.models import User


class OdinAuthBackend(AuthenticationBackend):

    async def authenticate(self, request: Request) -> typing.Optional[typing.Tuple['AuthCredentials', 'SimpleUser']]:
        if 'Authorization' not in request.headers:
            return

        return AuthCredentials(['mierda']), SimpleUser('su madre')
