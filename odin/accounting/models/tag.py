from gideon.fields import CharField
from gideon.models import Model


class Tag(Model):
    __table_name__ = 'tags'
    _name = CharField(name='name')
