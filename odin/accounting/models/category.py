from gideon.fields import CharField
from gideon.models import Model


class Category(Model):
    __table_name__ = 'categories'
    _name = CharField(name='name')
    _description = CharField(name='description')
