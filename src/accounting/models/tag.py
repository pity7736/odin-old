from src.db.fields import Field
from src.db.models import Model


class Tag(Model):
    __table_name__ = 'tags'
    id = Field(name='id')
    name = Field(name='name')
