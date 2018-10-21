from src.db.fields import Field
from src.db.models import Model


class Category(Model):
    __table_name__ = 'categories'
    id = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')

    @classmethod
    async def filter(cls, id=None, name=None, description=None):
        assert id or name or description, 'At least one parameter must be given.'
        con = await cls._get_connection()
        if id:
            field = 'id'
            value = id
        elif name:
            field = 'name'
            value = name
        else:
            field = 'description'
            value = description

        categories = await con.fetch(f'select * from categories where {field} = $1', value)
        await con.close()
        result = []
        for category in categories:
            result.append(Category(id=category['id'], name=category['name'], description=category['description']))
        return result
