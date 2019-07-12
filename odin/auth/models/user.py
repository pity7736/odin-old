from gideon.fields import CharField, DateTimeField
from gideon.models import Model

from odin.auth.utils import make_password


class User(Model):
    _email = CharField(name='email')
    _password = CharField(name='password')
    _created = DateTimeField(name='created', read_only=True)
    _first_name = CharField(name='first_name')
    _last_name = CharField(name='last_name')

    def set_password(self, raw_password):
        self._password = make_password(raw_password=raw_password)
