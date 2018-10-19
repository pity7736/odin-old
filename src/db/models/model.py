import asyncpg

from src import settings
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
        for key, value in self._fields.items():
            value = kwargs.get(key)
            setattr(self, key, value)

        for key, value in kwargs.items():
            if key not in self._fields.keys():
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
            if field.name != 'id':
                fields.append(field.name)
                values.append(f'${i}')
                arguments.append(getattr(self, field.name))
                i += 1

        fields = ', '.join(fields)
        values = ', '.join(values)
        sql = f'insert into {self.__table_name__}({fields}) values ({values}) RETURNING id'.replace("'", '')
        self.id = await con.fetchval(
            sql,
            *arguments
        )
        await con.close()
