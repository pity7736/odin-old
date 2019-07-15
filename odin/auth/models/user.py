from gideon.fields import CharField, DateTimeField
from gideon.models import Model

from odin.auth.utils import make_password
from .user_credential import UserCredentials


class User(Model):
    __table_name__ = 'users'
    _email = CharField(name='email')
    _password = CharField(name='password')
    _created = DateTimeField(name='created', read_only=True)
    _first_name = CharField(name='first_name')
    _last_name = CharField(name='last_name')

    async def set_password(self, raw_password):
        self._password, salt = make_password(raw_password=raw_password)
        user_credentials = UserCredentials(email=self._email, salt=salt)
        await user_credentials.save()
