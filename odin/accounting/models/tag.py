from gideon.fields import Field
from gideon.models import Model


class Tag(Model):
    __table_name__ = 'tags'
    _name = Field(name='name')
