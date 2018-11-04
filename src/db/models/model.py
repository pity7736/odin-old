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
        con = await self._get_connection()
        sql = f'insert into {self.__table_name__}({fields}) values ({values}) RETURNING id'.replace("'", '')
        self.id = await con.fetchval(sql, *arguments)
        await con.close()

    @classmethod
    async def get(cls, **kwargs):
        fields = []
        for i, key in enumerate(kwargs.keys(), start=1):
            fields.append(f'{key} = ${i}')

        fields = ' AND '.join(fields)
        sql = f'select * from {cls.__table_name__} where {fields}'
        con = await cls._get_connection()
        record = await con.fetchrow(sql, *kwargs.values())
        await con.close()
        if record:
            return cls(**record)

    @classmethod
    async def filter(cls, **kwargs):
        assert kwargs, 'keyword arguments are obligatory. If you want all records, use all method instead.'
        fields = []
        for i, field in enumerate(kwargs.keys(), start=1):
            fields.append(f'{field} = ${i}')

        fields = ' AND '.join(fields)
        connection = await cls._get_connection()
        records = await connection.fetch(f'select * from {cls.__table_name__} where {fields}', *kwargs.values())
        await connection.close()
        result = []
        for record in records:
            result.append(cls(**record))
        return result

    @classmethod
    async def all(cls):
        connection = await cls._get_connection()
        records = await connection.fetch(f'select * from {cls.__table_name__}')
        await connection.close()
        result = []
        for record in records:
            result.append(cls(**record))
        return result

    @staticmethod
    async def _get_connection():
        # TODO: refactor this. it should not be here
        return await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )
