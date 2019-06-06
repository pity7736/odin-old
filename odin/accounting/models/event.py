from gideon.fields import CharField, DateTimeField
from gideon.models import Model


class Event(Model):
    __table_name__ = 'events'
    _name = CharField(name='name')
    _init_date = DateTimeField(name='init_date')
    _end_date = DateTimeField(name='end_date')
