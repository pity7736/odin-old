import asyncio
from typing import Tuple, Optional

from odin.auth.models import User, UserCredential
from odin.auth.utils import make_password


class LoginController:

    def __init__(self, email: str, password: str):
        self._email = email
        self._password = password

    async def login(self) -> Tuple[Optional[str], str]:
        user, user_credential = await asyncio.gather(
            User.get(email=self._email),
            UserCredential.get(email=self._email)
        )
        if user is None:
            return None, f'Does not exists an user with email: {self._email}'

        encrypted_password = make_password(raw_password=self._password, salt=user_credential.salt)[0]
        token = None
        message = 'email or password are wrong'
        if encrypted_password == user.password:
            token = 'hola'
            message = 'login successfully'

        return token, message
