import asyncpg

from src import settings
from src.db.fields import Field
from src.db.models import Model


class Category(Model):
    __table_name__ = 'categories'
    id = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')

    @classmethod
    async def get(cls, id):
        con = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )
        record = await con.fetchrow(
            'select * from categories where id = $1',
            id
        )
        await con.close()
        if record:
            category = cls(id=id, name=record['name'], description=record['description'])
            return category

    @classmethod
    async def filter(cls, id=None, name=None, description=None):
        assert id or name or description, 'At least one parameter must be given.'
        con = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )
        if id:
            field = 'id'
            value = id
        elif name:
            field = 'name'
            value = name
        else:
            field = 'description'
            value = description

        categories = await con.fetch(
            f'select * from categories where {field} = $1',
            value
        )
        await con.close()
        result = []
        for category in categories:
            result.append(Category(id=category['id'], name=category['name'], description=category['description']))
        return result
