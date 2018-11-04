from src.db.fields import Field
from src.db.models import Model


class Category(Model):
    __table_name__ = 'categories'
    id = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')
