import asyncpg

from src import settings
from src.db.fields import ForeignKeyField
from src.db.fields.field import Field


class MetaModel(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        # TODO: use inmmutable map lib
        assert '__table_name__' in namespace, 'All model must have a __table_name__ attribute'
        fields = {}
        for attr, value in namespace.items():
            if isinstance(value, Field):
                fields[attr] = value

        model = type.__new__(mcs, name, bases, namespace)
        model._fields = fields
        return model


class Model(metaclass=MetaModel):

    __table_name__ = ''

    def __init__(self, **kwargs):
        for key, field in self._fields.items():
            value = kwargs.get(key)
            setattr(self, key, value)
            if isinstance(field, ForeignKeyField):
                setattr(self, f'{key}_id', None)

        for key, value in kwargs.items():
            if key not in self._fields.keys() and key not in vars(self):
                raise TypeError(f'Invalid field: {key} is not a field of {self.__class__}')
            setattr(self, key, value)

    async def save(self):
        con = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )
        fields = []
        values = []
        arguments = []
        i = 1
        for field in self._fields.values():
            field_name = field.name
            if field_name != 'id':
                if isinstance(field, ForeignKeyField):
                    instance = getattr(self, field_name)
                    field_name = f'{field_name}_id'
                    if instance:
                        setattr(self, field_name, instance.id)

                fields.append(field_name)
                values.append(f'${i}')
                arguments.append(field.to_db(getattr(self, field_name)))
                i += 1

        fields = ', '.join(fields)
        values = ', '.join(values)
        sql = f'insert into {self.__table_name__}({fields}) values ({values}) RETURNING id'.replace("'", '')
        self.id = await con.fetchval(
            sql,
            *arguments
        )
        await con.close()
